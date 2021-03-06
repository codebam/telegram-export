"""Utility functions for telegram-export which aren't specific to one purpose"""
from telethon.tl import types


ENTITY_TO_TEXT = {
    types.MessageEntityPre: 'pre',
    types.MessageEntityCode: 'code',
    types.MessageEntityBold: 'bold',
    types.MessageEntityItalic: 'italic',
    types.MessageEntityTextUrl: 'texturl',
    types.MessageEntityMentionName: 'mentionname'
}

TEXT_TO_ENTITY = {v: k for k, v in ENTITY_TO_TEXT.items()}


def encode_msg_entities(entities):
    """
    Encodes a list of MessageEntity into a string so it
    can easily be dumped into e.g. Dumper's database.
    """
    if not entities:
        return None
    parsed = []
    for entity in entities:
        if entity.__class__ in ENTITY_TO_TEXT:
            if isinstance(entity, types.MessageEntityTextUrl):
                extra = ',{}'.format(
                    entity.url.replace(',', '%2c').replace(';', '%3b')
                )
            elif isinstance(entity, types.MessageEntityMentionName):
                extra = ',{}'.format(entity.user_id)
            else:
                extra = ''
            parsed.append('{},{},{}{}'.format(
                ENTITY_TO_TEXT[type(entity)],
                entity.offset, entity.length, extra
            ))
    return ';'.join(parsed)


def decode_msg_entities(string):
    """
    Reverses the transformation made by ``utils.encode_msg_entities``.
    """
    if not string:
        return None
    parsed = []
    for part in string.split(';'):
        split = part.split(',')
        kind, offset, length = split[0], int(split[1]), int(split[2])
        if kind in TEXT_TO_ENTITY:
            if kind == 'texturl':
                parsed.append(types.MessageEntityTextUrl(
                    offset, length, split[-1]
                ))
            elif kind == 'mentionname':
                parsed.append(types.MessageEntityMentionName(
                    offset, length, int(split[-1])
                ))
            else:
                parsed.append(TEXT_TO_ENTITY[kind](offset, length))
    return parsed


def action_to_name(action):
    """
    Returns a namespace'd "friendly" name for the given
    ``MessageAction`` or ``ChannelAdminLogEventAction``.
    """
    return {
        types.MessageActionChannelCreate: 'channel.create',
        types.MessageActionChannelMigrateFrom: 'channel.migratefrom',
        types.MessageActionChatAddUser: 'chat.adduser',
        types.MessageActionChatCreate: 'chat.create',
        types.MessageActionChatDeletePhoto: 'chat.deletephoto',
        types.MessageActionChatDeleteUser: 'chat.deleteuser',
        types.MessageActionChatEditPhoto: 'chat.editphoto',
        types.MessageActionChatEditTitle: 'chat.edittitle',
        types.MessageActionChatJoinedByLink: 'chat.joinedbylink',
        types.MessageActionChatMigrateTo: 'chat.migrateto',
        types.MessageActionCustomAction: 'custom',
        types.MessageActionEmpty: 'empty',
        types.MessageActionGameScore: 'game.score',
        types.MessageActionHistoryClear: 'history.clear',
        types.MessageActionPaymentSent: 'payment.sent',
        types.MessageActionPaymentSentMe: 'payment.sentme',
        types.MessageActionPhoneCall: 'phone.call',
        types.MessageActionPinMessage: 'pin.message',
        types.MessageActionScreenshotTaken: 'screenshottaken',

        types.ChannelAdminLogEventActionChangeAbout: 'change.about',
        types.ChannelAdminLogEventActionChangePhoto: 'change.photo',
        types.ChannelAdminLogEventActionChangeStickerSet: 'change.stickerset',
        types.ChannelAdminLogEventActionChangeTitle: 'change.title',
        types.ChannelAdminLogEventActionChangeUsername: 'change.username',
        types.ChannelAdminLogEventActionDeleteMessage: 'delete.message',
        types.ChannelAdminLogEventActionEditMessage: 'edit.message',
        types.ChannelAdminLogEventActionParticipantInvite: 'participant.invite',
        types.ChannelAdminLogEventActionParticipantJoin: 'participant.join',
        types.ChannelAdminLogEventActionParticipantLeave: 'participant.leave',
        types.ChannelAdminLogEventActionParticipantToggleAdmin: 'participant.toggleadmin',
        types.ChannelAdminLogEventActionParticipantToggleBan: 'participant.toggleban',
        types.ChannelAdminLogEventActionToggleInvites: 'toggle.invites',
        types.ChannelAdminLogEventActionTogglePreHistoryHidden: 'toggle.prehistoryhidden',
        types.ChannelAdminLogEventActionToggleSignatures: 'toggle.signatures',
        types.ChannelAdminLogEventActionUpdatePinned: 'update.pinned',
    }.get(type(action), None)
