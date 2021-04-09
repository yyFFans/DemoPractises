# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'L3FileTransfer.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import json
import os
import sys
import paramiko
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import shutil
from traceback import extract_tb
from copy import deepcopy
import img
from subprocess import *


def extractExceptionInfo():
    ex_info = sys.exc_info()
    detailed_tb_info = extract_tb(ex_info[2], limit=2)
    internalException = ("detailed traceback info: File %s line %d, in %s" %
                         (os.path.basename(detailed_tb_info[1][0]),
                          detailed_tb_info[1][1],
                          detailed_tb_info[1][2]))
    internalException += ("%s" % detailed_tb_info[1][3])
    internalException += ("%s %s\n\n\n" % (str(ex_info[0]), str(ex_info[1])))
    return internalException


def open_ssh(configure):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=configure["ServerIP"], port=22, username=configure["UserName"],
                password=configure["PassWD"])
    return ssh


FAILURE = 0
SUCCESS = 1

StatusSignal = "Status"
LogInfoSignal = "LogInfo"


def git_cmd_exec(git_cmd):
    startupinfo = STARTUPINFO()
    startupinfo.dwFlags |= STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = SW_HIDE
    p = Popen("cmd", stdin=PIPE, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
    cmd_outs, cmd_errs = p.communicate(git_cmd)
    p.terminate()
    return cmd_outs


def git_status_parsing():
    new_files = set([])
    files_del = set([])
    files_mod = set([])

    outs = git_cmd_exec(b'git status\n')

    for line in outs.decode(encoding='utf-8', errors='ignore').split('\n'):
        if 'modified' in line:
            files_mod.add(line.split(':')[1].strip('\n').strip())
        if 'deleted' in line:
            files_del.add(line.split(':')[1].strip('\n').strip())
        if 'new file' in line:
            new_files.add(line.split(':')[1].strip('\n').strip())

    return new_files, files_del, files_mod


def ssh_exec_sudo_cmd(ssh, cmd, passwd):

    std_in, std_out, std_err = ssh.exec_command("sudo " + cmd, get_pty=True)

    std_in.write(passwd + '\n')
    # use thread to do sudo password checking, it's strange that no info in std_err
    # when cmd failed, all info is in std_out
    cmd_exe_info = ''
    #the following readline is to clear password checking msg
    std_out.readline()
    std_out.readline()

    for line in std_out:
        cmd_exe_info += line

    return cmd_exe_info


def ssh_exec_cmd(ssh, cmd):
    s_in, s_out, s_err = ssh.exec_command(cmd, timeout=600)

    err_info = s_err.read().decode('utf-8')
    if err_info != '':
        return FAILURE, "Error:exec {cmd} failed \n{info}\n". \
            format(cmd=cmd, info=err_info)
    return SUCCESS, s_out.read().decode('utf-8')


class UploadFilesThread(QtCore.QThread):
    logSignal = QtCore.pyqtSignal(str, str)
    threadOverSignal = QtCore.pyqtSignal()

    def __init__(self, ssh, ssh_sftp, upld_type, threadExceptionSignal, related_cfg):
        super(UploadFilesThread, self).__init__()
        self.cfg = related_cfg
        self.ssh = ssh
        self.ssh_sftp = ssh_sftp
        self.upld_type = upld_type
        self.LinuxHomeDir = '/home/' + self.cfg["UserName"] + '/'
        self.threadExceptionSignal = threadExceptionSignal

    def check_if_dir_need_upload(self, dir):
        need_upload = False
        for subdir in self.cfg["srcFileDirs"]:
            if subdir in dir:
                need_upload = True
                break

        if need_upload:
            for subdir in self.cfg["ignoredFileDirs"]:
                if subdir in dir:
                    return False
        else:
            return False
        return True

    def get_lowest_subdir(self, rootDir):
        already_append = False
        for file in os.listdir(rootDir):
            file = os.path.join(rootDir, file)
            if self.check_if_dir_need_upload(file):
                if os.path.isdir(file):
                    self.get_lowest_subdir(file)
                else:
                    if not already_append:
                        self.cfg["AllSubDirs"].add(rootDir)
                        already_append = True

    def compile(self):
        # clear local bin dirs on windows
        localBindir = self.cfg["CompileAndFetchBin"]["LocalBinDir"]
        if os.path.exists(localBindir):
            for file in os.listdir(localBindir):
                file = os.path.join(localBindir, file)
                if os.path.isdir(file):
                    shutil.rmtree(file)
                else:
                    os.remove(file)
        else:
            os.mkdir(localBindir)

        rrc_build_sh_path = (self.LinuxHomeDir + self.cfg["RemoteDir"] + '/' +
                             self.cfg["CompileAndFetchBin"][
                                 "BuildScriptDir"]).replace('\\', '/')
        succ_info = ""

        for script in self.cfg["CompileAndFetchBin"]["ShellScripts"]:
            exec_build_sh_cmd = "cd " + rrc_build_sh_path + ";" + \
                                "/bin/sh " + script + ";"

            ret, exec_info = ssh_exec_cmd(self.ssh, exec_build_sh_cmd)

            if FAILURE == ret:
                return FAILURE, exec_info + "\nExec {script} Failed\n".format(
                    script=script)
            else:
                succ_info += "Exec {script} success\n".format(script=script)

        return SUCCESS, succ_info

    def fetchBinFiles(self):
        # copy remote bins to local windows
        localBindir = self.cfg["CompileAndFetchBin"]["LocalBinDir"]
        bindir = self.cfg["CompileAndFetchBin"]["LinuxBinDir"]
        abslinuxbindir = self.LinuxHomeDir + self.cfg["RemoteDir"] + '/' + bindir

        ret, ret_info = ssh_exec_cmd(self.ssh, ("/bin/ls " + abslinuxbindir))

        # print(ret_info.split('\n'))

        for file in ret_info.split('\n'):
            if file == '':
                continue
            absfilename = abslinuxbindir + '/' + file
            localbinfile = os.path.join(localBindir, file)
            # print(abslinuxbindir)
            # print(localbinfile)
            self.ssh_sftp.get(absfilename, localbinfile)

    def upLoadfiles(self):
        for dir in self.cfg["AllSubDirs"]:
            split = self.cfg["LocalRepoDir"] + '\\'
            d = (self.cfg["RemoteDir"] + '/' + dir.split(split)[1]).replace('\\', '/')
            mk_dirs_cmd = "/bin/mkdir -p " + d
            ret, exec_info = ssh_exec_cmd(self.ssh, mk_dirs_cmd)
            if SUCCESS != ret:
                self.logSignal.emit(LogInfoSignal, exec_info)

            for file in os.listdir(dir):
                src_file = os.path.join(dir, file)
                if os.path.isfile(src_file):
                    dst_file = (os.path.
                                join(d, file)).replace('\\', '/')
                    # print(dst_file)
                    self.ssh_sftp.put(src_file, dst_file)

    def run(self):
        pwd = os.getcwd()
        try:
            if self.upld_type == "UpLdALL":
                # clear remote linux dirs
                self.cfg["AllSubDirs"] = set([])

                for dir in self.cfg["srcFileDirs"]:
                    self.get_lowest_subdir(dir)

                # remove repo root dir (always no src files)
                self.cfg["AllSubDirs"].remove(self.cfg["LocalRepoDir"])

                clear_remote_dirs_cmd = "/bin/rm -rf " + (
                    self.LinuxHomeDir + self.cfg["RemoteDir"])

                self.logSignal.emit(LogInfoSignal, "clear remote dirs\n")

                cmd_exe_info = ssh_exec_sudo_cmd(self.ssh, clear_remote_dirs_cmd,
                                                 self.cfg["PassWD"])

                if cmd_exe_info != '':
                    self.logSignal.emit(
                        LogInfoSignal, "Unexpected Error:clear remote dirs. {info}\n"
                            .format(info=cmd_exe_info))
                    self.logSignal.emit(StatusSignal, "Unexpected Error")
                    self.threadExceptionSignal.emit()
                    self.threadOverSignal.emit()
                    return

                self.logSignal.emit(StatusSignal, "Upload all files ongoing\n")

                self.upLoadfiles()

                self.logSignal.emit(LogInfoSignal, "Upload all file complete\n")

                # check if need compile
                if self.cfg["CompileAndFetchBin"]["Switch"] == "ON":
                    self.logSignal.emit(StatusSignal, "Compile ongoing\n")
                    ret, exec_info = self.compile()
                    if ret == SUCCESS:
                        self.logSignal.emit(LogInfoSignal, exec_info)

                        # compile Success Fetch the bin
                        self.logSignal.emit(StatusSignal, "fetch bin ongoing\n")
                        self.fetchBinFiles()
                        self.logSignal.emit(StatusSignal, "fetch bin complete.Idle\n")
                        self.logSignal.emit(
                            LogInfoSignal,
                            "fetch bin complete. please look up {dir} to confirm the bin "
                            "file\n".format(dir=self.cfg["CompileAndFetchBin"][
                                "LocalBinDir"]))
                        self.logSignal.emit(StatusSignal, "Idle\n")
                    else:
                        self.logSignal.emit(StatusSignal, "Compile failed.")
                        self.logSignal.emit(
                            LogInfoSignal,
                            "Check and fix the error,then you may click UpLDFixed\n")
                        self.logSignal.emit(LogInfoSignal, exec_info)
                else:
                    self.logSignal.emit(LogInfoSignal,
                                        "You have set CompileAndFetchBins Switch OFF, "
                                        "do not need compile\n")
                    self.logSignal.emit(StatusSignal, "compile switch off. Idle\n")

            if self.upld_type == "UpLdFixed":
                # upload fixed
                pwd = os.getcwd()
                os.chdir(self.cfg["LocalRepoDir"])

                # exec git add . for convenience of later git-status-parsing
                git_cmd_exec(b'git add .\n')

                self.logSignal.emit(LogInfoSignal, "checking git repo status\n")

                new_files, files_del, files_mod = git_status_parsing()
                # print "Repo files status"
                self.logSignal.emit(LogInfoSignal,
                                    "\nnew files:{files}\n".format(files=str(
                                        new_files)))

                self.logSignal.emit(LogInfoSignal,
                                    "\nfiles del:{files}\n".format(files=str(
                                        files_del)))

                self.logSignal.emit(LogInfoSignal,
                                    "\nfiles mod:{files}\n".format(files=str(
                                        files_mod)))

                self.logSignal.emit(StatusSignal, "Upload fixed files ongoing\n")

                for file in new_files:
                    remote_file = self.LinuxHomeDir + self.cfg["RemoteDir"] + '/' + file
                    local_file = os.path.join(self.cfg["LocalRepoDir"], file.replace('/',
                                                                                     '\\'))
                    self.ssh_sftp.put(local_file, remote_file)

                for file in files_del:
                    remote_file = self.LinuxHomeDir + self.cfg["RemoteDir"] + '/' + file
                    del_file_cmd = "/bin/rm -rf " + remote_file
                    ssh_exec_cmd(self.ssh, del_file_cmd)

                for file in files_mod:
                    local_file = os.path.join(self.cfg["LocalRepoDir"],
                                              file.replace('/', '\\'))
                    remote_file = self.LinuxHomeDir + self.cfg["RemoteDir"] + '/' + file
                    del_file_cmd = "/bin/rm -rf " + remote_file
                    ssh_exec_cmd(self.ssh, del_file_cmd)
                    self.ssh_sftp.put(local_file, remote_file)

                self.logSignal.emit(LogInfoSignal, "upload modified files completely\n")

                if self.cfg["CompileAndFetchBin"]["Switch"] == "ON":
                    self.logSignal.emit(StatusSignal, "Compile ongoing\n")
                    ret, exec_info = self.compile()
                    if SUCCESS == ret:
                        self.logSignal.emit(LogInfoSignal, exec_info)
                        # compile Success Fetch the bin
                        self.logSignal.emit(StatusSignal, "fetch bin ongoing\n")
                        self.fetchBinFiles()
                        self.logSignal.emit(StatusSignal, "fetch bin complete.Idle\n")
                        self.logSignal.emit(
                            LogInfoSignal,
                            "fetch bin complete. please look up {dir} to confirm the bin "
                            "file\n".format(dir=self.cfg["CompileAndFetchBin"][
                                "LocalBinDir"]))
                        self.logSignal.emit(StatusSignal, "Idle\n")
                    else:
                        self.logSignal.emit(StatusSignal, "Compile failed.\n")
                        self.logSignal.emit(
                            LogInfoSignal,
                            "Check and fix the error,then you may click UpLDFixed\n")
                        self.logSignal.emit(LogInfoSignal, exec_info)
                else:
                    self.logSignal.emit(LogInfoSignal,
                                        "You have set CompileAndFetchBins Switch OFF, "
                                        "do not need compile\n")
                    self.logSignal.emit(StatusSignal, "compile switch off. Idle\n")

                os.chdir(pwd)

            self.threadOverSignal.emit()
        except Exception:
            os.chdir(pwd)
            internalException = extractExceptionInfo()
            self.logSignal.emit(LogInfoSignal, internalException)
            self.logSignal.emit(StatusSignal, "Unexpected Internal Exception.\n")
            self.threadExceptionSignal.emit()
            self.threadOverSignal.emit()


class OpenSSHThread(QtCore.QThread):
    SSHOpenSignal = QtCore.pyqtSignal(paramiko.SSHClient, paramiko.SFTPClient)

    def __init__(self, cfg):
        super(OpenSSHThread, self).__init__()
        self.cfg = cfg

    def run(self):
        self.ssh = open_ssh(self.cfg)
        self.sftp = self.ssh.open_sftp()
        self.SSHOpenSignal.emit(self.ssh, self.sftp)


class Ui_L3SSHCrossCompile(QtWidgets.QMainWindow):
    internalExceptionSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(Ui_L3SSHCrossCompile, self).__init__()

        self.setObjectName("L3SSHCrossCompile")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setEnabled(True)
        self.resize(657, 765)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("python.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(':python.ico'))
        self.centralwidget = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.Configure = QtWidgets.QGroupBox(self.centralwidget)
        self.Configure.setEnabled(True)
        self.Configure.setGeometry(QtCore.QRect(20, 0, 651, 441))
        self.Configure.setObjectName("Configure")

        self.LinuxServerIP = QtWidgets.QLineEdit(self.Configure)
        self.LinuxServerIP.setGeometry(QtCore.QRect(140, 30, 141, 20))
        self.LinuxServerIP.setObjectName("LinuxServerIP")
        self.LinuxServerIP.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.LinuxServerIP.textChanged.connect(self.configureEdited)

        self.LinuxRemoteDir = QtWidgets.QLineEdit(self.Configure)
        self.LinuxRemoteDir.setGeometry(QtCore.QRect(390, 30, 231, 20))
        self.LinuxRemoteDir.setObjectName("LinuxRemoteDir")
        self.LinuxRemoteDir.textChanged.connect(self.configureEdited)

        self.PassWD = QtWidgets.QLineEdit(self.Configure)
        self.PassWD.setGeometry(QtCore.QRect(360, 60, 131, 20))
        self.PassWD.setObjectName("PassWD")
        self.PassWD.textChanged.connect(self.configureEdited)

        self.UserName = QtWidgets.QLineEdit(self.Configure)
        self.UserName.setGeometry(QtCore.QRect(140, 60, 121, 20))
        self.UserName.setObjectName("UserName")
        self.UserName.textChanged.connect(self.configureEdited)

        self.LocalRepoDir = QtWidgets.QLineEdit(self.Configure)
        self.LocalRepoDir.setGeometry(QtCore.QRect(140, 100, 401, 20))
        self.LocalRepoDir.setObjectName("LocalRepoDir")
        self.LocalRepoDir.textChanged.connect(self.configureEdited)

        self.LocalRepoDir.setReadOnly(True)

        self.LocalRepoDirLabel = QtWidgets.QLabel(self.Configure)
        self.LocalRepoDirLabel.setGeometry(QtCore.QRect(50, 100, 81, 21))
        self.LocalRepoDirLabel.setObjectName("LocalRepoDirLabel")

        self.BrowseFileButton = QtWidgets.QPushButton(self.Configure)
        self.BrowseFileButton.setGeometry(QtCore.QRect(560, 100, 51, 23))
        self.BrowseFileButton.setObjectName("BrowseFileButton")
        self.BrowseFileButton.clicked.connect(self.fileBrowsePressed)

        self.LinuxRemoteDirLabel = QtWidgets.QLabel(self.Configure)
        self.LinuxRemoteDirLabel.setGeometry(QtCore.QRect(300, 30, 91, 21))
        self.LinuxRemoteDirLabel.setObjectName("LinuxRemoteDirLabel")

        self.UserNamelabel = QtWidgets.QLabel(self.Configure)
        self.UserNamelabel.setGeometry(QtCore.QRect(63, 60, 61, 21))
        self.UserNamelabel.setObjectName("UserNamelabel")

        self.PassWDLabel = QtWidgets.QLabel(self.Configure)
        self.PassWDLabel.setGeometry(QtCore.QRect(310, 60, 54, 21))
        self.PassWDLabel.setObjectName("PassWDLabel")

        self.groupBox_2 = QtWidgets.QGroupBox(self.Configure)
        self.groupBox_2.setGeometry(QtCore.QRect(280, 140, 361, 291))
        self.groupBox_2.setObjectName("groupBox_2")
        self.CompileAndFetchBin = QtWidgets.QCheckBox(self.groupBox_2)
        self.CompileAndFetchBin.setGeometry(QtCore.QRect(10, 20, 131, 16))
        self.CompileAndFetchBin.setObjectName("CompileAndFetchBin")
        self.groupBox_2.setEnabled(True)

        self.BuildScriptDirLabel = QtWidgets.QLabel(self.groupBox_2)
        self.BuildScriptDirLabel.setGeometry(QtCore.QRect(10, 50, 91, 16))
        self.BuildScriptDirLabel.setObjectName("BuildScriptDirLabel")
        self.BuildScriptDir = QtWidgets.QLineEdit(self.groupBox_2)

        self.BuildScriptDir.setGeometry(QtCore.QRect(100, 50, 241, 20))
        self.BuildScriptDir.setObjectName("BuildScriptDir")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(10, 80, 91, 16))
        self.label_8.setObjectName("label_8")
        self.BuildScriptsText = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.BuildScriptsText.setGeometry(QtCore.QRect(10, 100, 341, 121))
        self.BuildScriptsText.setObjectName("BuildScriptsText")

        self.LocalSavingBinDir = QtWidgets.QLineEdit(self.groupBox_2)
        self.LocalSavingBinDir.setGeometry(QtCore.QRect(130, 260, 221, 20))
        self.LocalSavingBinDir.setObjectName("LocalSavingBinDir")
        self.LocalSavingBinDirLabel = QtWidgets.QLabel(self.groupBox_2)
        self.LocalSavingBinDirLabel.setGeometry(QtCore.QRect(10, 260, 111, 21))
        self.LocalSavingBinDirLabel.setObjectName("LocalSavingBinDirLabel")

        self.RemoteBinDir = QtWidgets.QLineEdit(self.groupBox_2)
        self.RemoteBinDir.setGeometry(QtCore.QRect(140, 230, 211, 20))
        self.RemoteBinDir.setObjectName("RemoteBinDir")
        self.RemoteOutputBinDirLabel = QtWidgets.QLabel(self.groupBox_2)
        self.RemoteOutputBinDirLabel.setGeometry(QtCore.QRect(10, 230, 121, 21))
        self.RemoteOutputBinDirLabel.setObjectName("RemoteOutputBinDirLabel")

        self.SubDirsNoNeedUpload = QtWidgets.QGroupBox(self.Configure)
        self.SubDirsNoNeedUpload.setEnabled(True)
        self.SubDirsNoNeedUpload.setGeometry(QtCore.QRect(10, 139, 251, 291))
        self.SubDirsNoNeedUpload.setObjectName("SubDirsNoNeedUpload")
        self.SubDirsNoNeedUploadText = QtWidgets.QPlainTextEdit(self.SubDirsNoNeedUpload)
        self.SubDirsNoNeedUploadText.setEnabled(True)
        self.SubDirsNoNeedUploadText.setGeometry(QtCore.QRect(10, 20, 231, 261))
        self.SubDirsNoNeedUploadText.setObjectName("SubDirsNoNeedUploadText")

        self.LinuxServerIPLabel = QtWidgets.QLabel(self.Configure)
        self.LinuxServerIPLabel.setGeometry(QtCore.QRect(50, 30, 81, 21))
        self.LinuxServerIPLabel.setObjectName("LinuxServerIPLabel")

        self.RunningLogs = QtWidgets.QGroupBox(self.centralwidget)
        self.RunningLogs.setGeometry(QtCore.QRect(20, 480, 511, 241))
        self.RunningLogs.setObjectName("RunningLogs")
        self.textBrowser = QtWidgets.QTextBrowser(self.RunningLogs)
        self.textBrowser.setGeometry(QtCore.QRect(10, 20, 491, 201))
        self.textBrowser.setObjectName("textBrowser")

        self.Action = QtWidgets.QGroupBox(self.centralwidget)
        self.Action.setEnabled(True)
        self.Action.setGeometry(QtCore.QRect(540, 480, 120, 241))
        self.Action.setObjectName("Action")

        self.UpLDAll = QtWidgets.QPushButton(self.Action)
        self.UpLDAll.setEnabled(False)
        self.UpLDAll.setGeometry(QtCore.QRect(10, 40, 101, 41))
        self.UpLDAll.setObjectName("UpLDAll")
        self.UpLDAll.clicked.connect(self.UploadAllSrcFilesPrepareProc)
        self.UpLDFixed = QtWidgets.QPushButton(self.Action)
        self.UpLDFixed.setEnabled(False)
        self.UpLDFixed.setGeometry(QtCore.QRect(10, 110, 101, 41))
        self.UpLDFixed.setObjectName("UpLDFixed")
        self.UpLDFixed.clicked.connect(self.UploadFixedFiles)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 740, 251, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bradley Hand ITC")
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName("label")

        self.Status = QtWidgets.QLineEdit(self.centralwidget)
        self.Status.setEnabled(True)
        self.Status.setGeometry(QtCore.QRect(80, 450, 571, 20))
        self.Status.setObjectName("Status")
        self.Status.setReadOnly(True)
        self.Status.setText("Configure not complete")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(33, 450, 41, 21))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Status")
        self.setCentralWidget(self.centralwidget)

        self.internalExceptionSignal.connect(self.internalExceptionProcess)

        self.retranslateUi()
        self.lastCfg = None
        # QtCore.QMetaObject.connectSlotsByName(self)
        try:
            self.loadCfg()
        except Exception:
            self.internalLogPrint("load cfg failed. please check your cfg\n")
            self.Status.setText("cfg error\n")

        self.CompileAndFetchBin.stateChanged.connect(self.CompileAndFetchBinSwitchChanged)

    def internalExceptionProcess(self):
        self.UpLDAll.setEnabled(True)
        self.Configure.setEnabled(True)

    def LogParsingShow(self, log_type, log_info):
        if log_type == StatusSignal:
            self.Status.setText(log_info)
            self.internalLogPrint(log_info)
        if log_type == LogInfoSignal:
            self.internalLogPrint(log_info)

    def uploadThreadOverProcess(self):
        self.UpLDAll.setEnabled(True)
        self.UpLDFixed.setEnabled(True)
        self.Configure.setEnabled(True)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("L3SSHCrossCompile", "L3CrossCompile"))
        self.Configure.setTitle(_translate("L3SSHCrossCompile", "Configure"))
        self.BrowseFileButton.setText(_translate("L3SSHCrossCompile", "Browse"))
        self.LinuxRemoteDirLabel.setText(
            _translate("L3SSHCrossCompile", "LinuxRemoteDir"))
        self.UserNamelabel.setText(_translate("L3SSHCrossCompile", "UserName"))
        self.PassWDLabel.setText(_translate("L3SSHCrossCompile", "PassWD"))
        self.groupBox_2.setTitle(_translate("L3SSHCrossCompile", "BuildSettings"))
        self.CompileAndFetchBin.setText(
            _translate("L3SSHCrossCompile", "CompileAndFetchBin"))
        self.BuildScriptDirLabel.setText(
            _translate("L3SSHCrossCompile", "BuildScriptDir"))
        self.label_8.setText(_translate("L3SSHCrossCompile", "BuildScripts"))
        self.LocalSavingBinDirLabel.setText(
            _translate("L3SSHCrossCompile", "LocalSavingBinDir"))
        self.RemoteOutputBinDirLabel.setText(
            _translate("L3SSHCrossCompile", "RemoteBinDir"))
        self.SubDirsNoNeedUpload.setTitle(
            _translate("L3SSHCrossCompile", "SubDirsNoNeedUpload"))
        self.LinuxServerIPLabel.setText(_translate("L3SSHCrossCompile", "LinuxServerIP"))
        self.LocalRepoDirLabel.setText(_translate("L3SSHCrossCompile", "LocalRepoDir"))
        self.RunningLogs.setTitle(_translate("L3SSHCrossCompile", "RunningLogs"))
        self.Action.setTitle(_translate("L3SSHCrossCompile", "Action"))
        self.UpLDAll.setText(_translate("L3SSHCrossCompile", "UpLDAll"))
        self.UpLDFixed.setText(_translate("L3SSHCrossCompile", "UpLDFixed"))
        self.label.setText(_translate("L3SSHCrossCompile",
                                      "Stay hungry, stay foolish. Make a difference."))
        self.Status.setText(_translate("L3SSHCrossCompile", "Status"))

    def loadCfg(self):
        self.cfgFile = open('cfg.json')
        self.cfg = json.load(self.cfgFile)
        self.LinuxServerIP.setText(self.cfg["ServerIP"])
        self.LinuxRemoteDir.setText(self.cfg["RemoteDir"])
        self.PassWD.setText(self.cfg["PassWD"])
        self.UserName.setText(self.cfg["UserName"])
        self.LocalRepoDir.setText(self.cfg["LocalRepoDir"])

        self.BuildScriptDir.setText(self.cfg["CompileAndFetchBin"]["BuildScriptDir"])

        for script in self.cfg["CompileAndFetchBin"]["ShellScripts"]:
            self.BuildScriptsText.appendPlainText(script)

        self.LocalSavingBinDir.setText(self.cfg["CompileAndFetchBin"]["LocalBinDir"])

        self.RemoteBinDir.setText(self.cfg["CompileAndFetchBin"]["LinuxBinDir"])

        if self.cfg["CompileAndFetchBin"]["Switch"] == 'ON':
            self.groupBox_2.setEnabled(True)
            self.CompileAndFetchBin.setCheckState(QtCore.Qt.Checked)
        else:
            self.BuildScriptDir.setEnabled(False)
            self.BuildScriptsText.setEnabled(False)
            self.LocalSavingBinDir.setEnabled(False)
            self.RemoteBinDir.setEnabled(False)
            self.CompileAndFetchBin.setCheckState(QtCore.Qt.Unchecked)

        for subdir in self.cfg["SubDirsNoNeedUpload"]:
            self.SubDirsNoNeedUploadText.appendPlainText(subdir)

        self.cfgFile.close()

    def saveCfg(self):
        self.cfg["ServerIP"] = self.LinuxServerIP.text()
        self.cfg["RemoteDir"] = self.LinuxRemoteDir.text()
        self.cfg["PassWD"] = self.PassWD.text()
        self.cfg["UserName"] = self.UserName.text()
        self.cfg["LocalRepoDir"] = self.LocalRepoDir.text()

        if self.CompileAndFetchBin.isChecked():
            self.cfg["CompileAndFetchBin"]["Switch"] = 'ON'
        else:
            self.cfg["CompileAndFetchBin"]["Switch"] = 'OFF'

        self.cfg["CompileAndFetchBin"]["BuildScriptDir"] = self.BuildScriptDir.text()

        self.cfg["SubDirsNoNeedUpload"] = []
        for text in self.SubDirsNoNeedUploadText.toPlainText().split('\n'):
            self.cfg["SubDirsNoNeedUpload"].append(text)

        self.cfg["CompileAndFetchBin"]["ShellScripts"] = []
        for text in self.BuildScriptsText.toPlainText().split('\n'):
            self.cfg["CompileAndFetchBin"]["ShellScripts"].append(text)

        self.cfg["CompileAndFetchBin"]["LinuxBinDir"] = self.RemoteBinDir.text()
        self.cfg["CompileAndFetchBin"]["LocalBinDir"] = self.LocalSavingBinDir.text()
        self.cfg["CompileAndFetchBin"]["BuildScriptDir"] = self.BuildScriptDir.text()

        with open('cfg.json', 'w') as f:
            json.dump(self.cfg, f, indent=4)

    def configureEdited(self):
        ip = self.LinuxServerIP.text()
        RemoteDir = self.LinuxRemoteDir.text()
        LocalRepoDir = self.LocalRepoDir.text()
        username = self.UserName.text()
        passwd = self.PassWD.text()

        if (ip != '' and RemoteDir != '' and LocalRepoDir != '' and username != ''
            and passwd != ''):
            self.Status.setText("Idle")

            self.UpLDAll.setEnabled(True)

            if self.lastCfg == None:
                return

            # check if LinuxRemoteDir LocalRepoDir has been changed
            if (self.lastCfg["LocalRepoDir"] != LocalRepoDir
                or self.lastCfg["RemoteDir"] != RemoteDir
                or self.lastCfg["ServerIP"] != ip
                or self.lastCfg["UserName"] != username):
                self.UpLDFixed.setEnabled(False)

        else:
            self.Status.setText("Configure not complete")
            self.UpLDAll.setEnabled(False)
            self.UpLDFixed.setEnabled(False)

    def CompileAndFetchBinSwitchChanged(self, state):
        self.UpLDFixed.setEnabled(False)
        if QtCore.Qt.Checked == state:
            self.BuildScriptDir.setEnabled(True)
            self.BuildScriptsText.setEnabled(True)
            self.RemoteBinDir.setEnabled(True)
            self.LocalSavingBinDir.setEnabled(True)
        else:
            self.BuildScriptDir.setEnabled(False)
            self.BuildScriptsText.setEnabled(False)
            self.RemoteBinDir.setEnabled(False)
            self.LocalSavingBinDir.setEnabled(False)

    def fileBrowsePressed(self):
        self.dirSelector = QtWidgets.QFileDialog()
        self.dirSelector.setGeometry(QtCore.QRect(20, 0, 651, 441))
        browsedir = (os.getcwd() if self.LocalRepoDir.text() == '' else self
                     .LocalRepoDir.text())
        dir = self.dirSelector.getExistingDirectory(
            self.centralwidget, "Select Directory", browsedir,
            QtWidgets.QFileDialog.ShowDirsOnly |
            QtWidgets.QFileDialog.DontResolveSymlinks)

        self.LocalRepoDir.setText(browsedir if dir == '' else dir)

    def internalLogPrint(self, text):
        self.textBrowser.insertPlainText(str(datetime.datetime.now()))
        self.textBrowser.insertPlainText('  ')
        self.textBrowser.insertPlainText(text)

    def updateRelatedCfg(self):
        self.related_cfg = deepcopy(self.cfg)
        self.related_cfg["srcFileDirs"] = []
        self.related_cfg["srcFileDirs"].append(self.cfg["LocalRepoDir"])

        self.related_cfg["ignoredFileDirs"] = []
        for dir in self.cfg["SubDirsNoNeedUpload"]:
            self.related_cfg["ignoredFileDirs"].append(
                os.path.join(self.cfg["LocalRepoDir"], dir))

    def UploadAllSrcFilesPrepareProc(self):
        try:
            self.UpLDAll.setEnabled(False)
            self.UpLDFixed.setEnabled(False)
            self.Configure.setEnabled(False)
            self.textBrowser.setText("")
            self.saveCfg()

            def is_cfg_modified(cfg, last_cfg):
                if (cfg["ServerIP"] != last_cfg["ServerIP"]
                    or cfg["UserName"] != last_cfg["UserName"]
                    or cfg["PassWD"] != last_cfg["PassWD"]):
                    return True
                return False

            if self.lastCfg == None:
                self.OpenSSHThread = OpenSSHThread(self.cfg)
                self.OpenSSHThread.SSHOpenSignal.connect(self.UploadAllSrcFiles)
                self.OpenSSHThread.start()
                self.internalLogPrint(
                "Connected to Server {ip}\n".format(ip=self.cfg["ServerIP"]))
            else:
                if is_cfg_modified(self.cfg, self.lastCfg):
                    self.ssh.close()
                    self.OpenSSHThread = OpenSSHThread(self.cfg)
                    self.OpenSSHThread.SSHOpenSignal.connect(self.UploadAllSrcFiles)
                    self.OpenSSHThread.start()
                    self.internalLogPrint(
                    "Connected to Server {ip}\n".format(ip=self.cfg["ServerIP"]))

                self.updateRelatedCfg()
                self.lastCfg = deepcopy(self.cfg)

                self.UploadFileThread = UploadFilesThread(
                    self.ssh, self.ssh_sftp, "UpLdALL", self.internalExceptionSignal,
                    self.related_cfg)
                self.UploadFileThread.threadOverSignal.connect(
                    self.uploadThreadOverProcess)
                self.UploadFileThread.logSignal.connect(self.LogParsingShow)

                self.UploadFileThread.start()

        except Exception:
            internalException = extractExceptionInfo()
            self.internalLogPrint(internalException)
            self.Status.setText("Unexpected Internal Exception.\n")
            self.internalExceptionSignal.emit()

    def UploadAllSrcFiles(self, ssh, sftp):
        try:
            self.ssh = ssh
            self.ssh_sftp = sftp

            self.updateRelatedCfg()
            self.lastCfg = deepcopy(self.cfg)

            self.UploadFileThread = UploadFilesThread(
                self.ssh, self.ssh_sftp, "UpLdALL", self.internalExceptionSignal,
                self.related_cfg)
            self.UploadFileThread.threadOverSignal.connect(self.uploadThreadOverProcess)
            self.UploadFileThread.logSignal.connect(self.LogParsingShow)

            self.UploadFileThread.start()
        except Exception:
            internalException = extractExceptionInfo()
            self.internalLogPrint(internalException)
            self.Status.setText("Unexpected Internal Exception.\n")
            self.internalExceptionSignal.emit()

    def UploadFixedFiles(self):
        try:
            self.UpLDAll.setEnabled(False)
            self.UpLDFixed.setEnabled(False)
            self.Configure.setEnabled(False)
            self.textBrowser.setText("")
            self.saveCfg()

            self.Status.setText("Upload fixed files ongoing\n")
            # upload fixed files
            self.updateRelatedCfg()
            self.lastCfg = deepcopy(self.cfg)
            self.UploadFileThread = UploadFilesThread(
                self.ssh, self.ssh_sftp, "UpLdFixed", self.internalExceptionSignal,
                self.related_cfg)

            self.UploadFileThread.threadOverSignal.connect(self.uploadThreadOverProcess)
            self.UploadFileThread.logSignal.connect(self.LogParsingShow)

            self.UploadFileThread.start()
        except Exception:
            internalException = extractExceptionInfo()
            self.internalLogPrint(internalException)
            self.Status.setText("Unexpected Internal Exception.\n")
            self.internalExceptionSignal.emit()


if __name__ == '__main__':
    env = os.environ
    if "QT_QPA_PLATFORM_PLUGIN_PATH" in env.keys():
        old_qt_path = env["QT_QPA_PLATFORM_PLUGIN_PATH"]
        try:
            if hasattr(sys, '_MEIPASS'):
                new_qt_path = sys._MEIPASS + '/PyQt5/Qt/plugins'
                env["QT_QPA_PLATFORM_PLUGIN_PATH"] = new_qt_path

            app = QtWidgets.QApplication(sys.argv)
            # print("running path {path}".format(path=app.libraryPaths()))
            MyUI = Ui_L3SSHCrossCompile()
            MyUI.setFixedSize(MyUI.width(), MyUI.height())
            MyUI.show()
            sys.exit(app.exec_())
        finally:
            env["QT_QPA_PLATFORM_PLUGIN_PATH"] = old_qt_path
    else:
        app = QtWidgets.QApplication(sys.argv)
        MyUI = Ui_L3SSHCrossCompile()
        MyUI.setFixedSize(MyUI.width(), MyUI.height())
        MyUI.show()
        sys.exit(app.exec_())
