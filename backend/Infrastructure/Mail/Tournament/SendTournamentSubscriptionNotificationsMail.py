from DataDomain.Database.Model import Tournaments, Users
from Infrastructure.Mail.Tournament import SendTournamentSubscriptionNotificationMail


class SendTournamentSubscriptionNotificationsMail:
    """Email all users about a tournament update."""

    @staticmethod
    def send(
            users: list[Users],
            tournament: Tournaments,
            message: str) -> None:

        [SendTournamentSubscriptionNotificationMail().send(user, tournament, message)
         for user in users]
