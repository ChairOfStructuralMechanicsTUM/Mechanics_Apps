from enum import Enum, unique


@unique
class ElSupEnum(Enum):
    SUPPORT_CLAMPED = 1  # vis + calc
    SUPPORT_NORMAL_FORCE = 1.1  # vis + calc
    SUPPORT_TRANSVERSE_FORCE = 1.2  # vis + calc
    SUPPORT_FIXED_END = 2  # calc
    SUPPORT_FIXED_CONTINUOUS = 2.1  # vis + calc
    SUPPORT_FIXED_JOINT = 2.2  # vis + calc
    SUPPORT_ROLLER_END = 3  # calc
    SUPPORT_ROLLER_CONTINUOUS = 3.1  # vis + calc
    SUPPORT_ROLLER_JOINT = 3.2  # vis + calc
    SPRING_SUPPORT = 4  # vis
    SPRING_MOMENT_SUPPORT = 4.1  # vis
    NODE = 5  # vis
    FREE_END = 5.1  # calc
    THROUGH_ELEMENT = 5.2  # calc
    JOINT = 6  # vis + calc
    JOINT_NORMAL_FORCE = 6.1  # vis + calc
    JOINT_TRANSVERSE_FORCE = 6.2  # vis + calc
    SPRING = 7  # vis + calc
    ROD = 8
    BEAM = 9  # vis
    LOAD_POINT = 10  # vis + calc
    LOAD_MOMENT = 11  # vis + calc
    LOAD_LINE = 12  # vis + calc
    LOAD_TEMP = 13  # vis + calc


def value_in_enum(enum, val):
    """
    checks, if a value is in an enum
    :param enum: enum to search in
    :param val: key or value to search for
    :return: boolean if found, key, value
    """
    if val in enum._value2member_map_:
        return True, enum(val).name, val
    elif val in enum.__members__:
        return True, val, enum[val].value
    else:
        return False, None, None


def get_enum_of_value(enum, val):
    """
    checks, if a value is in an enum, and if true, returns value
    :param enum: enum to search in
    :param val: key or value to search for
    :return: boolean if found, enum_of_val
    """
    if val in enum._value2member_map_:
        return True, enum(val)
    elif val in enum.__members__:
        return True, val, enum[val]
    else:
        return False, None


def check_val_in_enum_list(val_to_check, validate_list):
    """
    Checks, if a val_to_check is
     1.) in a enum (doesn't matter if val_to_check is key or value)
     2.) is in the validate_list
    """
    inside, val, key = value_in_enum(ElSupEnum, val_to_check)
    if val in validate_list:
        return True
    else:
        return False


def check_beams_and_rods(val_to_check):
    validate_list = [ElSupEnum.ROD.name, ElSupEnum.BEAM.name]
    return check_val_in_enum_list(val_to_check, validate_list)


def check_line_spring(val_to_check):
    validate_list = [ElSupEnum.SPRING.name]
    return check_val_in_enum_list(val_to_check, validate_list)


def check_point_spring(val_to_check):
    validate_list = [ElSupEnum.SPRING_MOMENT_SUPPORT.name, ElSupEnum.SPRING_SUPPORT.name]
    return check_val_in_enum_list(val_to_check, validate_list)


def check_line_load(val_to_check):
    validate_list = [ElSupEnum.LOAD_LINE.name]
    return check_val_in_enum_list(val_to_check, validate_list)


def check_point_load(val_to_check):
    validate_list = [ElSupEnum.LOAD_POINT.name, ElSupEnum.LOAD_MOMENT.name]
    return check_val_in_enum_list(val_to_check, validate_list)


def check_temp_load(val_to_check):
    validate_list = [ElSupEnum.LOAD_TEMP.name]
    return check_val_in_enum_list(val_to_check, validate_list)


def check_user_defined_load(val_to_check):
    validate_list = [-1] # TODO add correct value here
    return check_val_in_enum_list(val_to_check, validate_list)


if __name__ == "__main__":
    """
    Shows the possibilities to deal with the enum and get different output
    """
    # printing enum member as string
    print("The string representation of enum member is : ", end="")
    print(ElSupEnum.BEAM)

    # printing enum member as repr
    print("The repr representation of enum member is : ", end="")
    print(repr(ElSupEnum.BEAM))

    # printing the type of enum member using type()
    print("The type of enum member is : ", end="")
    print(type(ElSupEnum.BEAM))

    # printing name of enum member using "name" keyword
    print("The name of enum member is : ", end="")
    print(ElSupEnum.BEAM.name)

    # printing value of enum member using "value" keyword
    print("The value of enum member is : ", end="")
    print(ElSupEnum.BEAM.value)

    """ OUTPUT
    The string representation of enum member is : ElSupEnum.BEAM
    The repr representation of enum member is : <ElSupEnum.BEAM: 9>
    The type of enum member is : <enum 'ElSupEnum'>
    The name of enum member is : BEAM
    The value of enum member is : 9
    """
