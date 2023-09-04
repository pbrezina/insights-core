"""
UdevRules - files ``/usr/lib/udev/rules.d/*`` and ``/etc/udev/rules.d/``
========================================================================

The parsers included in this module are:

UdevRulesFCWWPN - file ``/usr/lib/udev/rules.d/59-fc-wwpn-id.rules``
--------------------------------------------------------------------

UdevRules40Redhat - files ``/etc/udev/rules.d/40-redhat.rules``, ``/run/udev/rules.d/40-redhat.rules``, ``/usr/lib/udev/rules.d/40-redhat.rules``, ``/usr/local/lib/udev/rules.d/40-redhat.rules``
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

UdevRulesOracleASM - file ``/etc/udev/rules.d/*asm*.rules``
-----------------------------------------------------------

UdevRules66MD - files ``/etc/udev/rules.d/66-md-auto-re-add.rules``, ``/usr/lib/udev/rules.d/66-md-auto-re-add.rules``
----------------------------------------------------------------------------------------------------------------------
"""
from insights import parser
from insights.core import LogFileOutput
from insights.specs import Specs


@parser(Specs.udev_fc_wwpn_id_rules)
class UdevRulesFCWWPN(LogFileOutput):
    """
    Read the content of ``/usr/lib/udev/rules.d/59-fc-wwpn-id.rules`` file.

    .. note::

        The syntax of the `.rules` file is complex, and no rules require to
        get the serialized parsed result currently.  An only existing rule's
        supposed to check the syntax of some specific line, so here the
        :class:`insights.core.LogFileOutput` is the base class.

    Examples:
        >>> type(udev_rules)
        <class 'insights.parsers.udev_rules.UdevRulesFCWWPN'>
        >>> 'ENV{FC_TARGET_WWPN}!="$*"; GOTO="fc_wwpn_end"' in udev_rules.lines
        True
    """
    pass


@parser(Specs.etc_udev_40_redhat_rules)
class UdevRules40Redhat(LogFileOutput):
    """
    Read the content of ``40-redhat.rules`` file.

    .. note::

        The syntax of the `.rules` file is complex, and no rules require to
        get the serialized parsed result currently.  An only existing rule's
        supposed to check the syntax of some specific line, so here the
        :class:`insights.core.LogFileOutput` is the base class.

    Sample input::

        # do not edit this file, it will be overwritten on update
        # CPU hotadd request
        SUBSYSTEM=="cpu", ACTION=="add", TEST=="online", ATTR{online}=="0", ATTR{online}="1"

        # Memory hotadd request
        SUBSYSTEM!="memory", ACTION!="add", GOTO="memory_hotplug_end"
        PROGRAM="/bin/uname -p", RESULT=="s390*", GOTO="memory_hotplug_end"

        LABEL="memory_hotplug_end"

    Examples:
        >>> 'LABEL="memory_hotplug_end"' in udev_40_redhat_rules.lines
        True
    """
    pass


@parser(Specs.etc_udev_oracle_asm_rules)
class UdevRulesOracleASM(LogFileOutput):
    """
    Read the content of ``/etc/udev/rules.d/*asm*.rules`` file.

    .. note::

        The syntax of the `.rules` file is complex, and no rules require to
        get the serialized parsed result currently.  An only existing rule's
        supposed to check the syntax of some specific lines, so here the
        :class:`insights.core.LogFileOutput` is the base class.

    Sample input::

        KERNEL=="dm*", PROGRAM=="scsi_id --page=0x83 --whitelisted --device=/dev/%k", \
        RESULT=="360060e80164c210000014c2100007a8f", \
        SYMLINK+="oracleasm/disks/asm_sbe80_7a8f", OWNER="oracle", GROUP="dba", MODE="0660"


        KERNEL=="dm*", PROGRAM=="scsi_id --page=0x83 --whitelisted --device=/dev/%k", \
        RESULT=="360060e80164c210000014c2100007a91", \
        SYMLINK+="oracleasm/disks/asm_sbe80_7a91", OWNER="oracle", GROUP="dba", MODE="0660"

        # NOTE: Insert new Oracle ASM LUN configuration before this comment
        ACTION=="add|change", KERNEL=="sd*", OPTIONS:="nowatch"

    Examples:

    >>> 'ACTION=="add|change", KERNEL=="sd*", OPTIONS:="nowatch"' in udev_oracle_asm_rules.lines
    True
    >>> udev_oracle_asm_rules.get('ACTION')[0]['raw_message']
    'ACTION=="add|change", KERNEL=="sd*", OPTIONS:="nowatch"'
    """
    pass


@parser(Specs.udev_66_md_rules)
class UdevRules66MD(LogFileOutput):
    """
    Read the content of ``66-md-auto-re-add.rules`` file.

    .. note::

        The syntax of the `.rules` file is complex, and no rules require to
        get the serialized parsed result currently.  This udev rule file is
        collected with filters for some specific lines. Using
        :class:`insights.core.LogFileOutput` as the base class here.

    Sample input::

        # Enable/Disable - default is Disabled
        # to disable this rule, GOTO="md_end" should be the first active command.
        # to enable this rule, Comment out GOTO="md_end".
        GOTO="md_end"

        ACTION!="add", GOTO="md_end"
        ENV{ID_FS_TYPE}!="linux_raid_member", GOTO="md_end"
        SUBSYSTEM=="block", ACTION=="add", RUN{program}+="/sbin/md_raid_auto_readd.sh $devnode"

        #
        # Land here to exit cleanly
        LABEL="md_end"

    Examples:
        >>> 'GOTO="md_end"' in udev_66_md_rules.lines
        True
    """
    pass
