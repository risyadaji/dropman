def genMessageFormat(actionType, data):
  if (actionType == "toggle"):
    return '''
    > **Type**: {type}
    > **Status**: {status}
    > **Started At**: {startedAt}
    '''.format(type=data['type'], status=data['status'], startedAt=data['startedAt'])

  if (actionType == "getlist"):
    return '''
    > **{name}**
    > **ID**: {id}
    > **Memory**: {memory}
    > **Disk**: {disk}
    > **CPU**: {cpu}
    > **Status**: {status}
    '''.format(name=data['name'], id=data['id'], memory=data['memory'], disk=data['disk'], cpu=data['vcpus'], status=data['status'])

  return ""
