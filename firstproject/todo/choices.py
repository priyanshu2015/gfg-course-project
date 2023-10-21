class TaskStatusChoice:
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"

    CHOICE_LIST = [
        (PENDING, PENDING),
        (IN_PROGRESS, IN_PROGRESS),
        (DONE, DONE),
        (ARCHIVED, ARCHIVED)
    ]