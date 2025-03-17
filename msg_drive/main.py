from typing import List
from dataclasses import dataclass

import apos
from apos.interfaces import (
    ICommand,
    ICommandHandler,
    IEvent,
    IEventHandler,
    IQuery,
    IQueryHandler,
)


@dataclass
class RegisterUserCommand(ICommand):
    email: str


@dataclass
class UserRegisteredEvent(IEvent):
    email: str


@dataclass
class NewUserGreetedEvent(IEvent):
    email: str


@dataclass
class RegisterUserQuery(IQuery):
    email: str


class BaseEventPublisher:
    _messager: apos.Apos

    def __init__(self, messenger: apos.Apos) -> None:
        self._messenger = messenger


class RegisterUser(BaseEventPublisher, ICommandHandler):
    def __call__(self, command: RegisterUserCommand) -> None:
        self._messenger.publish_event(UserRegisteredEvent(command.email))


class GreetNewUser(BaseEventPublisher, IEventHandler):
    def __call__(self, event: UserRegisteredEvent) -> None:
        self._messenger.publish_event(NewUserGreetedEvent(event.email))


# class ...(BaseEventPublisher, IQueryHandler):
#     def __call__(self, query: RegisterUserQuery) -> str:
#         return f"Hello {query.email}"


def main():
    bus = apos.Apos()

    register_user = RegisterUser(bus)
    greet_new_user = GreetNewUser(bus)

    bus.subscribe_command(RegisterUserCommand, register_user)
    bus.subscribe_event(UserRegisteredEvent, [greet_new_user])
    # bus.subscribe_query(RegisterUserQuery, register_user)

    bus.publish_command(RegisterUserCommand(email="TakiMoysha"))
    events: List[apos.IEvent] = bus.get_published_events()
    print("All events: ", events)

    response = bus.publish_query(RegisterUserQuery(email="TakiMoysha"))
    print(response, type(response))

    # bus.publish_event()

    # apos.publish_event(UserDeactivatedEvent(user_name="Max"))
    # apos.subscribe_event(UserDeactivatedEvent, [withdraw_job_applications])


if __name__ == "__main__":
    main()
