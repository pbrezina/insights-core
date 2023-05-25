import doctest

from insights.combiners import os_release
from insights.combiners.os_release import OSRelease
from insights.parsers.dmesg import DmesgLineList
from insights.parsers.installed_rpms import InstalledRpms
from insights.parsers.os_release import OsRelease as OSReleaseParser
from insights.parsers.redhat_release import RedhatRelease
from insights.parsers.uname import Uname
from insights.tests import context_wrap

UNAME_86 = "Linux vm-123 4.18.0-372.19.1.el8_6.x86_64 #1 SMP Mon Jul 18 11:14:02 EDT 2022 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_91 = "Linux vm-123 5.14.0-162.6.1.el9_1.x86_64 #1 SMP PREEMPT_DYNAMIC Fri Sep 30 07:36:03 EDT 2022 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_CENTOS_7_9 = "Linux kvm-01-guest17.lab.eng.brq2.redhat.com 3.10.0-1160.el7.x86_64 #1 SMP Mon Oct 19 16:18:59 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_CENTOS_8_5 = "Linux kvm-02-guest12.rhts.eng.brq.redhat.com 4.18.0-348.7.1.el8_5.x86_64 #1 SMP Wed Dec 22 13:25:12 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_CENTOS_9STR = "Linux hpe-apollo-cn99xx-15-vm-17.khw4.lab.eng.bos.redhat.com 5.14.0-316.el9.aarch64 #1 SMP PREEMPT_DYNAMIC Fri May 19 12:15:43 UTC 2023 aarch64 aarch64 aarch64 GNU/Linux"
UNAME_ORACLE = "Linux atlnfs4testd 4.18.0-372.19.1.el8_6uek.x86_64 #1 SMP Thu Nov 7 17:01:44 PST 2013 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_FEDORA = "Linux sironote.home.local 3.17.8-200.fc20.x86_64 #1 SMP Thu Jan 8 23:26:57 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_UNKNOWN = "Linux eslinb24.emea.nsn-net.net 2.6.39.4-9.NSN.kiuas #1 SMP Thu Feb 13 08:58:31 EET 2014 x86_64 x86_64 x86_64 GNU/Linux"

RPMS_JSON_91_WO_KERNEL = '''
{"name":"audit-libs", "epoch":"(none)", "version":"11", "release":"13.el9", "arch":"noarch", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Sat Nov 20 18:50:43 2021, Key ID 199e2f91fd431d51"}
{"name":"basesystem", "epoch":"(none)", "version":"11", "release":"13.el9", "arch":"noarch", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Sat Nov 20 18:50:43 2021, Key ID 199e2f91fd431d51"}
{"name":"bash", "epoch":"(none)", "version":"5.1.8", "release":"5.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Thu Aug 25 21:46:10 2022, Key ID 199e2f91fd431d51"}
{"name":"coreutils", "epoch":"(none)", "version":"8.32", "release":"32.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Thu Jun 16 12:19:44 2022, Key ID 199e2f91fd431d51"}
{"name":"dbus", "epoch":"1", "version":"1.12.20", "release":"6.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Tue Aug 23 23:01:36 2022, Key ID 199e2f91fd431d51"}
{"name":"dmidecode", "epoch":"1", "version":"3.3", "release":"7.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Tue Mar 15 15:41:19 2022, Key ID 199e2f91fd431d51"}
{"name":"dnf", "epoch":"(none)", "version":"057", "release":"13.git20220816.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Wed Aug 17 08:06:56 2022, Key ID 199e2f91fd431d51"}
{"name":"dracut", "epoch":"(none)", "version":"057", "release":"13.git20220816.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Wed Aug 17 08:06:56 2022, Key ID 199e2f91fd431d51"}
{"name":"filesystem", "epoch":"(none)", "version":"3.16", "release":"2.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Sat Nov 20 19:51:43 2021, Key ID 199e2f91fd431d51"}
{"name":"firewalld", "epoch":"(none)", "version":"1.1.1", "release":"3.el9", "arch":"noarch", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Mon Aug  8 21:31:26 2022, Key ID 199e2f91fd431d51"}
{"name":"glibc", "epoch":"(none)", "version":"2.34", "release":"40.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Thu Jul 28 15:15:24 2022, Key ID 199e2f91fd431d51"}
{"name":"gmp", "epoch":"1", "version":"6.2.0", "release":"10.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Sun Nov 21 16:04:10 2021, Key ID 199e2f91fd431d51"}
{"name":"libacl", "epoch":"(none)", "version":"2.3.1", "release":"3.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Sun Nov 21 08:14:00 2021, Key ID 199e2f91fd431d51"}
{"name":"libgcc", "epoch":"(none)", "version":"11.3.1", "release":"2.1.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Thu Jul 14 22:56:25 2022, Key ID 199e2f91fd431d51"}
{"name":"libselinux", "epoch":"(none)", "version":"3.4", "release":"3.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Tue Jul 26 15:17:57 2022, Key ID 199e2f91fd431d51"}
{"name":"systemd", "epoch":"(none)", "version":"250", "release":"12.el9_1", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Thu 29 Sep 2022 05:02:47 PM CST, Key ID 199e2f91fd431d51"}
'''.strip()
RPMS_JSON_91_W_KERNEL = RPMS_JSON_91_WO_KERNEL + """
{"name":"passwd", "epoch":"(none)", "version":"3.4", "release":"4.el9", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Tue Sep 13 16:46:26 2022, Key ID 199e2f91fd431d51"}
{"name":"kernel", "epoch":"(none)", "version":"5.14.0", "release":"70.13.1.el9_0", "arch":"x86_64", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Mon 05 Sep 2022 09:55:09 PM CST, Key ID 199e2f91fd431d51"}
{"name":"kernel", "epoch":"(none)", "version":"5.14.0", "release":"162.6.1.el9_1", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Mon 03 Oct 2022 04:18:36 PM CST, Key ID 199e2f91fd431d51"}"""
RPMS_JSON_8_NG = '''
{"name":"kernel", "epoch":"(none)", "version":"4.18.0", "release":"425.3.1.el8", "arch":"x86_64", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Tue Nov  8 18:10:54 2022, Key ID 99e2f91fd431d51"}
{"name":"kernel", "epoch":"(none)", "version":"4.18.0", "release":"372.19.1.el8_6uek", "arch":"x86_64", "vendor":"Oracle America", "sigpgp":"RSA/SHA256, Wed Sep 15 17:11:22 2021, Key ID 99e2f91fd431d51"}
{"name":"kernel", "epoch":"(none)", "version":"4.18.0", "release":"372.19.1.el8_6", "arch":"x86_64", "vendor":"SUSE, Inc.", "sigpgp":"RSA/SHA256, Wed Sep 15 17:11:22 2021, Key ID 99e2f91fd431d51"}
{"name":"libselinux", "epoch":"(none)", "version":"2.9", "release":"6.el8", "arch":"i686", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Mon 15 Aug 2022 08:55:09 PM CST, Key ID 99e2f91fd431d51"}
{"name":"dbus", "epoch":"1", "version":"1.12.8", "release":"23.el8", "arch":"x86_64", "vendor":"Red, Inc.", "sigpgp":"RSA/SHA256, Wed 07 Sep 2022 04:08:12 AM CST, Key ID 99e2f91fd431d51"}
{"name":"dracut", "epoch":"(none)", "version":"049", "release":"209.git20220815.el8", "arch":"x86_64", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Mon 15 Aug 2022 09:56:58 PM CST, Key ID 99e2f91fd431d51"}
{"name":"libgcc", "epoch":"(none)", "version":"8.5.0", "release":"15.el8", "arch":"x86_64", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Thu 21 Jul 2022 05:36:25 PM CST, Key ID 99e2f91fd431d51"}
{"name":"policycoreutils", "epoch":"(none)", "version":"2.9", "release":"20.el8", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Mon 15 Aug 2022 08:51:06 PM CST, Key ID 199e2f91fd431d51"}
{"name":"glibc", "epoch":"(none)", "version":"2.28", "release":"211.el8", "arch":"x86_64", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Mon 29 Aug 2022 04:13:20 PM CST, Key ID 99e2f91fd431d51"}
{"name":"libacl", "epoch":"(none)", "version":"2.2.53", "release":"1.el8", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Sat 15 Dec 2018 05:44:36 AM CST, Key ID 199e2f91fd431d51"}
{"name":"glibc", "epoch":"(none)", "version":"2.28", "release":"211.el8", "arch":"i686", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Mon 29 Aug 2022 04:12:26 PM CST, Key ID 99e2f91fd431d51"}
{"name":"libgcc", "epoch":"(none)", "version":"8.5.0", "release":"15.el8", "arch":"i686", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Thu 21 Jul 2022 05:36:01 PM CST, Key ID 199e2f91fd431d51"}
{"name":"bash", "epoch":"(none)", "version":"4.4.20", "release":"4.el8_6", "arch":"x86_64", "vendor":"RHat, Inc.", "sigpgp":"RSA/SHA256, Mon 20 Jun 2022 09:20:51 PM CST, Key ID 99e2f91fd431d51"}
{"name":"libselinux", "epoch":"(none)", "version":"2.9", "release":"6.el8", "arch":"x86_64", "vendor":"Hat, Inc.", "sigpgp":"RSA/SHA256, Mon 15 Aug 2022 08:55:11 PM CST, Key ID 09e2f91fd431d51"}
{"name":"coreutils", "epoch":"(none)", "version":"8.30", "release":"13.el8", "arch":"x86_64", "vendor":"Hat, Inc.", "sigpgp":"RSA/SHA256, Thu 16 Jun 2022 12:18:02 PM CST, Key ID 09e2f91fd431d51"}
{"name":"firewalld", "epoch":"(none)", "version":"0.9.3", "release":"13.el8", "arch":"noarch", "vendor":"Red, Inc.", "sigpgp":"RSA/SHA256, Fri 25 Feb 2022 09:40:17 PM CST, Key ID 09e2f91fd431d51"}
{"name":"filesystem", "epoch":"(none)", "version":"3.8", "release":"6.el8", "arch":"x86_64", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Mon 21 Jun 2021 07:17:43 PM CST, Key ID 99e2f91fd431d51"}
{"name":"gmp", "epoch":"1", "version":"6.1.2", "release":"10.el8", "arch":"x86_64", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Fri 14 Jun 2019 04:58:39 PM CST, Key ID 99e2f91fd431d51"}
{"name":"basesystem", "epoch":"(none)", "version":"11", "release":"5.el8", "arch":"noarch", "vendor":"RH, Inc.", "sigpgp":"RSA/SHA256, Sat 15 Dec 2018 05:49:21 AM CST, Key ID 09e2f91fd431d51"}
{"name":"dmidecode", "epoch":"1", "version":"3.3", "release":"4.el8", "arch":"x86_64", "vendor":"Red, Inc.", "sigpgp":"RSA/SHA256, Mon 14 Mar 2022 02:13:06 PM CST, Key ID 99e2f91fd431d51"}
'''.strip()
RPMS_JSON_9_NG_RH_KERNEL = RPMS_JSON_8_NG + """
{"name":"kernel", "epoch":"(none)", "version":"5.14.0", "release":"162.6.1.el9_1", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Mon 03 Oct 2022 04:18:36 PM CST, Key ID 199e2f91fd431d51"}"""
RPMS_JSON_ROCKY = '''
{"name":"rocky-release", "epoch":"1", "version":"3.3", "release":"4.el8", "arch":"x86_64", "vendor":"Red Hat, Inc.", "sigpgp":"RSA/SHA256, Mon 14 Mar 2022 02:13:06 PM CST, Key ID 99e2f91fd431d51"}
'''.strip()
RPMS_CENTOS_7_9_RAW = '''
glibc-common-2.17-317.el7.x86_64
dracut-config-rescue-033-572.el7.x86_64
dracut-033-572.el7.x86_64
dbus-libs-1.10.24-15.el7.x86_64
systemd-sysv-219-78.el7.x86_64
dracut-network-033-572.el7.x86_64
python-slip-dbus-0.4.0-4.el7.noarch
firewalld-filesystem-0.6.3-11.el7.noarch
libgcc-4.8.5-44.el7.x86_64
filesystem-3.2-25.el7.x86_64
glibc-2.17-317.el7.x86_64
libselinux-2.5-15.el7.x86_64
libacl-2.2.51-15.el7.x86_64
fontpackages-filesystem-1.44-8.el7.noarch
libselinux-utils-2.5-15.el7.x86_64
gmp-6.0.0-15.el7.x86_64
coreutils-8.22-24.el7.x86_64
rpm-libs-4.11.3-45.el7.x86_64
dmidecode-3.2-5.el7.x86_64
systemd-libs-219-78.el7.x86_64
systemd-219-78.el7.x86_64
policycoreutils-2.5-34.el7.x86_64
dbus-python-1.1.1-9.el7.x86_64
rpm-build-libs-4.11.3-45.el7.x86_64
yum-plugin-fastestmirror-1.1.31-54.el7_8.noarch
firewalld-0.6.3-11.el7.noarch
vim-filesystem-7.4.629-8.el7_9.x86_64
basesystem-10.0-7.el7.centos.noarch
bash-4.2.46-34.el7.x86_64
emacs-filesystem-24.3-23.el7.noarch
yum-metadata-parser-1.1.4-10.el7.x86_64
libselinux-python-2.5-15.el7.x86_64
rpm-4.11.3-45.el7.x86_64
dbus-1.10.24-15.el7.x86_64
dbus-glib-0.100-7.el7.x86_64
rpm-python-4.11.3-45.el7.x86_64
yum-3.4.3-168.el7.centos.noarch
'''
RPMS_CENTOS_9STR_RAW = '''
libgcc-11.3.1-4.4.el9.aarch64
libreport-filesystem-2.15.2-6.el9.noarch
dnf-data-4.14.0-4.el9.noarch
fonts-filesystem-2.0.5-7.el9.1.noarch
firewalld-filesystem-1.2.1-1.el9.noarch
coreutils-common-8.32-34.el9.aarch64
filesystem-3.16-2.el9.aarch64
efi-filesystem-4-8.el9.noarch
basesystem-11-13.el9.noarch
glibc-gconv-extra-2.34-68.el9.aarch64
glibc-langpack-en-2.34-68.el9.aarch64
glibc-common-2.34-68.el9.aarch64
glibc-2.34-68.el9.aarch64
bash-5.1.8-6.el9.aarch64
gmp-6.2.0-10.el9.aarch64
libselinux-3.5-1.el9.aarch64
libacl-2.3.1-3.el9.aarch64
coreutils-8.32-34.el9.aarch64
systemd-libs-252-8.el9.aarch64
dbus-libs-1.12.20-7.el9.aarch64
python3-systemd-234-18.el9.aarch64
libselinux-utils-3.5-1.el9.aarch64
systemd-rpm-macros-252-8.el9.noarch
dmidecode-3.3-7.el9.aarch64
dbus-1.12.20-7.el9.aarch64
systemd-pam-252-8.el9.aarch64
systemd-252-8.el9.aarch64
dbus-common-1.12.20-7.el9.noarch
dbus-broker-28-7.el9.aarch64
python3-dbus-1.2.18-2.el9.aarch64
systemd-udev-252-8.el9.aarch64
dracut-057-21.git20230214.el9.aarch64
dracut-network-057-21.git20230214.el9.aarch64
dracut-squash-057-21.git20230214.el9.aarch64
rpm-libs-4.16.1.3-22.el9.aarch64
rpm-4.16.1.3-22.el9.aarch64
policycoreutils-3.5-1.el9.aarch64
rpm-plugin-systemd-inhibit-4.16.1.3-22.el9.aarch64
rpm-build-libs-4.16.1.3-22.el9.aarch64
rpm-sign-libs-4.16.1.3-22.el9.aarch64
python3-rpm-4.16.1.3-22.el9.aarch64
libdnf-0.69.0-3.el9.aarch64
python3-libdnf-0.69.0-3.el9.aarch64
python3-dnf-4.14.0-4.el9.noarch
dnf-4.14.0-4.el9.noarch
python3-dnf-plugins-core-4.3.0-4.el9.noarch
dnf-plugins-core-4.3.0-4.el9.noarch
yum-4.14.0-4.el9.noarch
rpm-plugin-selinux-4.16.1.3-22.el9.aarch64
rpm-plugin-audit-4.16.1.3-22.el9.aarch64
dracut-config-rescue-057-21.git20230214.el9.aarch64
firewalld-1.2.1-1.el9.noarch
python3-libselinux-3.5-1.el9.aarch64
xdg-dbus-proxy-0.1.3-1.el9.aarch64
emacs-filesystem-27.2-9.el9.noarch
vim-filesystem-8.2.2637-20.el9.noarch
hunspell-filesystem-1.7.0-11.el9.aarch64
python3-policycoreutils-3.5-1.el9.noarch
policycoreutils-python-utils-3.5-1.el9.noarch
'''
RPMS_CENTOS_8_5_RAW = '''
dbus-glib-0.110-2.el8.x86_64
dnf-data-4.7.0-4.el8.noarch
dracut-squash-049-191.git20210920.el8.x86_64
dbus-common-1.12.8-14.el8.noarch
basesystem-11-5.el8.noarch
libselinux-2.9-5.el8.x86_64
glibc-langpack-en-2.28-164.el8.x86_64
rpm-plugin-systemd-inhibit-4.14.3-19.el8.x86_64
glibc-2.28-164.el8.x86_64
dracut-network-049-191.git20210920.el8.x86_64
python3-libdnf-0.63.0-3.el8.x86_64
python3-rpm-4.14.3-19.el8.x86_64
gmp-6.1.2-10.el8.x86_64
python3-dnf-4.7.0-4.el8.noarch
python3-dnf-plugins-core-4.0.21-3.el8.noarch
firewalld-0.9.3-7.el8.noarch
yum-4.7.0-4.el8.noarch
libacl-2.2.53-1.el8.x86_64
dracut-config-rescue-049-191.git20210920.el8.x86_64
dmidecode-3.2-10.el8.x86_64
coreutils-common-8.30-12.el8.x86_64
libselinux-utils-2.9-5.el8.x86_64
rpm-4.14.3-19.el8.x86_64
dbus-tools-1.12.8-14.el8.x86_64
systemd-libs-239-51.el8_5.2.x86_64
dbus-daemon-1.12.8-14.el8.x86_64
systemd-pam-239-51.el8_5.2.x86_64
dbus-1.12.8-14.el8.x86_64
systemd-udev-239-51.el8_5.2.x86_64
policycoreutils-2.9-16.el8.x86_64
libgcc-8.5.0-4.el8_5.x86_64
python3-dbus-1.2.4-15.el8.x86_64
libreport-filesystem-2.9.5-15.el8.x86_64
firewalld-filesystem-0.9.3-7.el8.noarch
filesystem-3.8-6.el8.x86_64
glibc-common-2.28-164.el8.x86_64
bash-4.4.20-2.el8.x86_64
libdnf-0.63.0-3.el8.x86_64
rpm-build-libs-4.14.3-19.el8.x86_64
dnf-4.7.0-4.el8.noarch
python3-libselinux-2.9-5.el8.x86_64
python3-slip-dbus-0.6.4-11.el8.noarch
dnf-plugins-core-4.0.21-3.el8.noarch
dbus-libs-1.12.8-14.el8.x86_64
coreutils-8.30-12.el8.x86_64
rpm-libs-4.14.3-19.el8.x86_64
dracut-049-191.git20210920.el8.x86_64
systemd-239-51.el8_5.2.x86_64
rpm-plugin-selinux-4.14.3-19.el8.x86_64
'''

DMESG_ORACLE = """
Linux version kernel-4.18.0-372.19.1.el8_6uek.x86_64 (mockbuild@ca-build56.us.oracle.com) (gcc version 4.1.2 20080704 (Red Hat 4.1.2-54)) #1 SMP Mon Sep 30 16:46:32 PDT 2013
""".strip()
DMESG_CENTOS_7_9 = """
[    0.000000] Initializing cgroup subsys cpuset
[    0.000000] Initializing cgroup subsys cpu
[    0.000000] Initializing cgroup subsys cpuacct
[    0.000000] Linux version 3.10.0-1160.el7.x86_64 (mockbuild@kbuilder.bsys.centos.org) (gcc version 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC) ) #1 SMP Mon Oct 19 16:18:59 UTC 2020
[    0.000000] Command line: initrd=/images/kvm-01-guest17.lab.eng.brq2.redhat.com/initrd console=ttyS0,115200 ks=http://beaker.engineering.redhat.com/kickstart/11931405 ksdevice=bootif netboot_method=pxe BOOT_IMAGE=/images/kvm-01-guest17.lab.eng.brq2.redhat.com/kernel BOOTIF=01-52-54-00-d4-b4-e6
""".strip()
DMESG_CENTOS_8_5 = """
[    0.000000] Linux version 4.18.0-240.el8.x86_64 (mockbuild@kbuilder.bsys.centos.org) (gcc version 8.4.1 20200928 (Red Hat 8.4.1-1) (GCC)) #1 SMP Tue Apr 13 16:24:22 UTC 2021
""".strip()
DMESG_CENTOS_9STR = """
[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x431f0af1]
[    0.000000] Linux version 5.14.0-316.el9.aarch64 (mockbuild@aarch64-01.stream.rdu2.redhat.com) (gcc (GCC) 11.3.1 20221121 (Red Hat 11.3.1-4), GNU ld version 2.35.2-39.el9) #1 SMP PREEMPT_DYNAMIC Fri May 19 12:15:43 UTC 2023
[    0.000000] The list of certified hardware and cloud instances for Red Hat Enterprise Linux 9 can be viewed at the Red Hat Ecosystem Catalog, https://catalog.redhat.com.
"""
DMESG_SUSE = """
Linux version 2.6.32-431.23.3.el6.x86_64 (sandman@ceph01t6) (gcc version 4.4.7 20120313 (Novell 4.4.7-4) (GCC) ) #1 SMP Tue Jul 29 17:05:14 EDT 2014
""".strip()
DMESG_UNKNOWN = """
Linux version 2.6.32-431.17.1.el6.x86_64 (mockbuild@lxdist01) (gcc version 4.4.7 20120313 (Red Hat 4.4.7-4) (GCC) ) #1 SMP Thu May 8 08:33:50 CEST 2014
""".strip()
DMESG_NG = """
Initializing cgroup subsys cpu
Command line: ro root=/dev/vg00/lvol1
""".strip()
DMESG_REDHAT = """
[    0.000000] Linux version 5.14.0-162.6.1.el9_1.x86_64 (mockbuild@x86-vm-07.build.eng.bos.redhat.com) (gcc (GCC) 11.3.1 20220421 (Red Hat 11.3.1-2), GNU ld version 2.35.2-24.el9) #1 SMP PREEMPT_DYNAMIC Tue Dec 20 06:06:30 EST 2022
""".strip()


REDHAT_RELEASE_86 = "Red Hat Enterprise Linux release 8.6 (Ootpa)"
REDHAT_RELEASE_FEDORA = "Fedora release 23 (Twenty Three)"
REDHAT_RELEASE_UNKNOWN = "Test OS"
REDHAT_RELEASE_CENTOS_9STR = "CentOS Stream release 9"

OS_RELEASE_RH = """
NAME="Red Hat Enterprise Linux"
ID="rhel"
""".strip()
OS_RELEASE_OL = """
NAME="Oracle Linux Server"
ID="ol"
PRETTY_NAME="Red Hat Enterprise Linux"
""".strip()
OS_RELEASE_CENTOS_9STR = """
NAME="CentOS Stream"
VERSION="9"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="9"
PLATFORM_ID="platform:el9"
PRETTY_NAME="CentOS Stream 9"
ANSI_COLOR="0;31"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:centos:centos:9"
HOME_URL="https://centos.org/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux 9"
REDHAT_SUPPORT_PRODUCT_VERSION="CentOS Stream"
"""
OS_RELEASE_UNKNOWN = """
NAME="Test OS"
ID="test"
PRETTY_NAME="Test OS"
""".strip()


def test_is_rhel():
    # RHEL, uname only
    uname = Uname(context_wrap(UNAME_91))
    result = OSRelease(uname, None, None, None, None)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.reasons == {}

    # RHEL, dmesg only
    dmesg = DmesgLineList(context_wrap(DMESG_REDHAT))
    result = OSRelease(None, dmesg, None, None, None)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.product == "RHEL"
    assert result.reasons == {}

    # RHEL, dmesg and uname
    dmesg = DmesgLineList(context_wrap(DMESG_REDHAT))
    result = OSRelease(uname, dmesg, None, None, None)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.reasons == {}

    # RHEL, rpms only
    rpms = InstalledRpms(context_wrap(RPMS_JSON_91_WO_KERNEL))
    result = OSRelease(None, None, rpms, None, None)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.reasons == {}

    rpms = InstalledRpms(context_wrap(RPMS_JSON_91_W_KERNEL))
    result = OSRelease(None, None, rpms, None, None)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.reasons == {}

    # RHEL, rpms and uname
    rpms = InstalledRpms(context_wrap(RPMS_JSON_91_W_KERNEL))
    result = OSRelease(uname, None, rpms, None, None)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.reasons == {}

    # RHEL, rpms, dmesg and uname
    rpms = InstalledRpms(context_wrap(RPMS_JSON_91_W_KERNEL))
    result = OSRelease(uname, dmesg, rpms, None, None)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.reasons == {}

    # RHEL, os-release
    osr = OSReleaseParser(context_wrap(OS_RELEASE_RH))
    result = OSRelease(None, None, None, osr, None)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.reasons == {}

    # RHEL, redhat-release
    rhr = RedhatRelease(context_wrap(REDHAT_RELEASE_86))
    result = OSRelease(None, None, None, None, rhr)
    assert result.is_rhel is True
    assert result.release == "RHEL"
    assert result.reasons == {}


def test_not_rhel_failures():
    # NON-RHEL: Nothing
    result = OSRelease(None, None, None, None, None)
    assert result.is_rhel is False
    assert result.release == "Unknown"
    assert result.reasons.get('reason') == "Nothing available to check"

    # NON-RHEL: BAD rpms
    rpms = InstalledRpms(context_wrap(RPMS_JSON_ROCKY))
    result = OSRelease(None, None, rpms, None, None)
    assert result.is_rhel is False
    assert result.release == "Rocky"
    assert result.reasons['release'] == 'rocky-release-3.3-4.el8'

    # NON-RHEL: BAD rpms, too many faulty pkgs
    rpms = InstalledRpms(context_wrap(RPMS_JSON_8_NG))
    result = OSRelease(None, None, rpms, None, None)
    assert result.is_rhel is False
    assert result.release == "Unknown"
    assert result.reasons['faulty_packages'] == [
        'basesystem-11-5.el8', 'bash-4.4.20-4.el8_6',
        'coreutils-8.30-13.el8', 'dbus-1.12.8-23.el8',
        'dmidecode-3.3-4.el8', 'dracut-049-209.git20220815.el8',
        'filesystem-3.8-6.el8', 'firewalld-0.9.3-13.el8',
        'glibc-2.28-211.el8', 'gmp-6.1.2-10.el8',
        'libgcc-8.5.0-15.el8', 'libselinux-2.9-6.el8']

    # NON-RHEL: BAD rpms, too many faulty, but running kernel is from Red Hat
    rpms = InstalledRpms(context_wrap(RPMS_JSON_9_NG_RH_KERNEL))
    uname = Uname(context_wrap(UNAME_91))
    result = OSRelease(uname, None, rpms, None, None)
    assert result.is_rhel is False
    assert result.release == "Unknown"
    assert result.reasons['faulty_packages'] == [
        'basesystem-11-5.el8', 'bash-4.4.20-4.el8_6',
        'coreutils-8.30-13.el8', 'dbus-1.12.8-23.el8',
        'dmidecode-3.3-4.el8', 'dracut-049-209.git20220815.el8',
        'filesystem-3.8-6.el8', 'firewalld-0.9.3-13.el8',
        'glibc-2.28-211.el8', 'gmp-6.1.2-10.el8',
        'libgcc-8.5.0-15.el8', 'libselinux-2.9-6.el8']

    # NON-RHEL: BAD rpms with uname
    uname = Uname(context_wrap(UNAME_86))
    result = OSRelease(uname, None, rpms, None, None)
    assert result.is_rhel is False
    assert result.release == "SUSE"
    assert result.reasons['kernel_vendor'] == 'SUSE, Inc.'
    assert result.reasons['faulty_packages'] == [
        'basesystem-11-5.el8', 'bash-4.4.20-4.el8_6',
        'coreutils-8.30-13.el8', 'dbus-1.12.8-23.el8',
        'dmidecode-3.3-4.el8', 'dracut-049-209.git20220815.el8',
        'filesystem-3.8-6.el8', 'firewalld-0.9.3-13.el8',
        'glibc-2.28-211.el8', 'gmp-6.1.2-10.el8',
        'kernel-4.18.0-372.19.1.el8_6', 'libgcc-8.5.0-15.el8',
        'libselinux-2.9-6.el8']

    # NON-RHEL: BAD dmesg
    dmesg = DmesgLineList(context_wrap(DMESG_NG))
    result = OSRelease(None, dmesg, None, None, None)
    assert result.is_rhel is False
    assert result.release == "Unknown"
    assert result.reasons.get('reason') == "Nothing available to check"

    dmesg = DmesgLineList(context_wrap(DMESG_SUSE))
    result = OSRelease(None, dmesg, None, None, None)
    assert result.is_rhel is False
    assert result.release == "SUSE"
    assert result.reasons['build_info'] == DMESG_SUSE

    # NON-RHEL: unknown dmesg alone
    dmesg = DmesgLineList(context_wrap(DMESG_UNKNOWN))
    result = OSRelease(None, dmesg, None, None, None)
    assert result.is_rhel is False
    assert result.release == "Unknown"
    assert result.reasons['build_info'] == DMESG_UNKNOWN

    # NON-RHEL: BAD uname
    uname = Uname(context_wrap(UNAME_ORACLE))
    result = OSRelease(uname, None, None, None, None)
    assert result.is_rhel is False
    assert result.release == "Oracle"
    assert result.reasons.get('kernel') == "4.18.0-372.19.1.el8_6uek.x86_64"

    uname = Uname(context_wrap(UNAME_FEDORA))
    result = OSRelease(uname, None, None, None, None)
    assert result.is_rhel is False
    assert result.release == "Fedora"
    assert result.reasons.get('kernel') == "3.17.8-200.fc20.x86_64"

    uname = Uname(context_wrap(UNAME_UNKNOWN))
    result = OSRelease(uname, None, None, None, None)
    assert result.is_rhel is False
    assert result.release == "Unknown"
    assert result.reasons.get('kernel') == "2.6.39.4-9.NSN.kiuas"

    # NON-RHEL: Bad Uname + Dmesg
    dmesg = DmesgLineList(context_wrap(DMESG_NG))
    uname = Uname(context_wrap(UNAME_ORACLE))
    result = OSRelease(uname, dmesg, None, None, None)
    assert result.is_rhel is False
    assert result.release == "Oracle"
    assert result.reasons['kernel'] == "4.18.0-372.19.1.el8_6uek.x86_64"

    dmesg = DmesgLineList(context_wrap(DMESG_ORACLE))
    result = OSRelease(uname, dmesg, None, None, None)
    assert result.is_rhel is False
    assert result.release == "Oracle"
    assert result.reasons['build_info'] == DMESG_ORACLE
    assert result.reasons['kernel'] == "4.18.0-372.19.1.el8_6uek.x86_64"
    assert 'kernel_vendor' not in result.reasons  # No RPMs

    # NON-RHEL: Bad Dmesg + RPMs
    dmesg = DmesgLineList(context_wrap(DMESG_SUSE))
    rpms = InstalledRpms(context_wrap(RPMS_JSON_8_NG))
    result = OSRelease(None, dmesg, rpms, None, None)
    assert result.is_rhel is False
    assert result.release == "SUSE"  # from Dmesg
    assert result.reasons['build_info'] == DMESG_SUSE  # from Dmesg
    assert 'kernel' not in result.reasons  # No Uname
    assert 'kernel_vendor' not in result.reasons  # No Uname

    # NON-RHEL: Bad Uname + Dmesg + RPMs
    dmesg = DmesgLineList(context_wrap(DMESG_ORACLE))
    uname = Uname(context_wrap(UNAME_86))
    rpms = InstalledRpms(context_wrap(RPMS_JSON_8_NG))
    result = OSRelease(uname, dmesg, rpms, None, None)
    assert result.is_rhel is False
    assert result.release == "SUSE"  # from Dmesg first then updated by RPMS
    assert result.reasons['build_info'] == DMESG_ORACLE  # from Dmesg
    assert 'kernel' not in result.reasons  # Uname is OK
    assert result.reasons['kernel_vendor'] == "SUSE, Inc."

    dmesg = DmesgLineList(context_wrap(DMESG_ORACLE))
    uname = Uname(context_wrap(UNAME_UNKNOWN))
    rpms = InstalledRpms(context_wrap(RPMS_JSON_8_NG))
    result = OSRelease(uname, dmesg, rpms, None, None)
    assert result.is_rhel is False
    assert result.release == "Oracle"  # from Dmesg
    assert result.reasons['build_info'] == DMESG_ORACLE  # from Dmesg
    assert result.reasons.get('kernel') == "2.6.39.4-9.NSN.kiuas"
    assert 'kernel_vendor' not in result.reasons  # running kernel not in RPMs

    dmesg = DmesgLineList(context_wrap(DMESG_ORACLE))
    uname = Uname(context_wrap(UNAME_ORACLE))
    result = OSRelease(uname, dmesg, rpms, None, None)
    assert result.is_rhel is False
    assert result.release == "Oracle"
    assert result.reasons['build_info'] == DMESG_ORACLE
    assert result.reasons['kernel'] == "4.18.0-372.19.1.el8_6uek.x86_64"
    assert result.reasons['kernel_vendor'] == "Oracle America"
    assert result.reasons['faulty_packages'] == [
        'basesystem-11-5.el8', 'bash-4.4.20-4.el8_6',
        'coreutils-8.30-13.el8', 'dbus-1.12.8-23.el8',
        'dmidecode-3.3-4.el8', 'dracut-049-209.git20220815.el8',
        'filesystem-3.8-6.el8', 'firewalld-0.9.3-13.el8',
        'glibc-2.28-211.el8', 'gmp-6.1.2-10.el8',
        'kernel-4.18.0-372.19.1.el8_6uek',
        'libgcc-8.5.0-15.el8', 'libselinux-2.9-6.el8']

    # RHEL, Bad os-release only
    osr = OSReleaseParser(context_wrap(OS_RELEASE_UNKNOWN))
    result = OSRelease(None, None, None, osr, None)
    assert result.is_rhel is False
    assert result.release == "Test OS"
    assert result.reasons == {'reason': 'NON-RHEL: os-release/redhat-release'}

    osr = OSReleaseParser(context_wrap(OS_RELEASE_OL))
    result = OSRelease(None, None, None, osr, None)
    assert result.is_rhel is False
    assert result.release == "Oracle Linux Server"
    assert result.reasons == {'reason': 'NON-RHEL: os-release/redhat-release'}

    # RHEL, redhat-release
    rhr = RedhatRelease(context_wrap(REDHAT_RELEASE_FEDORA))
    result = OSRelease(None, None, None, None, rhr)
    assert result.is_rhel is False
    assert result.release == "Fedora"
    assert result.reasons == {'reason': 'NON-RHEL: os-release/redhat-release'}

    rhr = RedhatRelease(context_wrap(REDHAT_RELEASE_UNKNOWN))
    result = OSRelease(None, None, None, None, rhr)
    assert result.is_rhel is False
    assert result.release == "Test OS"
    assert result.reasons == {'reason': 'NON-RHEL: os-release/redhat-release'}


def test_centos():
    # CentOS checks
    dmesg = DmesgLineList(context_wrap(DMESG_CENTOS_7_9))
    uname = Uname(context_wrap(UNAME_CENTOS_7_9))
    result = OSRelease(None, dmesg, None, None, None)
    assert not result.is_rhel
    assert result.is_convert2rhelable
    assert result.release == "CentOS"
    assert result.reasons['build_info'] == DMESG_CENTOS_7_9.splitlines()[3]
    result = OSRelease(uname, dmesg, None, None, None)
    assert not result.is_rhel
    assert result.is_convert2rhelable
    assert result.release == "CentOS"
    assert result.reasons['build_info'] == DMESG_CENTOS_7_9.splitlines()[3]
    # CentOS uname is exactly the same as RHEL - if that's all we have to go
    # on then we can't tell.
    result = OSRelease(uname, None, None, None, None)
    assert result.is_rhel
    assert not result.is_convert2rhelable
    assert result.release == "RHEL"
    assert 'build_info' not in result.reasons

    dmesg = DmesgLineList(context_wrap(DMESG_CENTOS_8_5))
    uname = Uname(context_wrap(UNAME_CENTOS_8_5))
    result = OSRelease(None, dmesg, None, None, None)
    assert not result.is_rhel
    assert result.is_convert2rhelable
    assert result.release == "CentOS"
    assert result.reasons['build_info'] == DMESG_CENTOS_8_5
    result = OSRelease(uname, dmesg, None, None, None)
    assert not result.is_rhel
    assert result.is_convert2rhelable
    assert result.release == "CentOS"
    assert result.reasons['build_info'] == DMESG_CENTOS_8_5
    # CentOS uname is exactly the same as RHEL - if that's all we have to go
    # on then we can't tell.
    result = OSRelease(uname, None, None, None, None)
    assert result.is_rhel
    assert not result.is_convert2rhelable
    assert result.release == "RHEL"
    assert 'build_info' not in result.reasons

    dmesg = DmesgLineList(context_wrap(DMESG_CENTOS_9STR))
    uname = Uname(context_wrap(UNAME_CENTOS_9STR))
    rpms = InstalledRpms(context_wrap(RPMS_CENTOS_9STR_RAW))
    redhat_release = RedhatRelease(context_wrap(REDHAT_RELEASE_CENTOS_9STR))
    os_release = OSReleaseParser(context_wrap(OS_RELEASE_CENTOS_9STR))
    # From dmesg alone, because CentOS 9 is now compiled by redhat.com
    # servers, we can't determine if its CentOS or RHEL
    result = OSRelease(None, dmesg, None, None, None)
    assert result.is_rhel
    assert not result.is_convert2rhelable
    assert result.release == "RHEL"
    # and uname is not enough to differentiate either
    result = OSRelease(uname, dmesg, None, None, None)
    assert result.is_rhel
    assert not result.is_convert2rhelable
    assert result.release == "RHEL"
    # and even rpms can't help
    result = OSRelease(uname, dmesg, rpms, None, None)
    assert result.is_rhel
    assert not result.is_convert2rhelable
    assert result.release == "RHEL"


def test_osr_doc():
    dmesg = DmesgLineList(context_wrap(DMESG_ORACLE))
    uname = Uname(context_wrap(UNAME_ORACLE))
    rpms = InstalledRpms(context_wrap(RPMS_JSON_8_NG))
    env = {
        'osr': OSRelease(uname, dmesg, rpms, None, None),
    }
    failed, total = doctest.testmod(os_release, globs=env)
    assert failed == 0
