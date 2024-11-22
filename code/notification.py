from abc import ABC, abstractmethod

class Observer(ABC):
    """Observer interface for all user classes."""
    @abstractmethod
    def update(self, message):
        pass

class Subject(ABC):
    """Subject interface for managing observers."""
    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self, message):
        pass

class Notification(Subject):
    _user_notifications = {}  # Shared dictionary for all user notifications

    def __init__(self, username):
        self.username = username
        # Initialize a notification list for the user if not already present
        if username not in Notification._user_notifications:
            Notification._user_notifications[username] = []
        self.observers = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def add_notification(self, message):
        """Add a general notification for this user, ensuring duplicates are not added."""
        # Check if the message already exists in the user's notifications
        existing_notifications = Notification._user_notifications.get(self.username, [])
        
        # Check if any existing notification has the same message
        if not any(notification["message"] == message for notification in existing_notifications):
            # If the message is not found, add the new notification
            Notification._user_notifications[self.username].append({"message": message, "is_new": True})
            self.notify_observers(message)
        

    def add_notification_for_observer(self, message, target_username):
        """Send a notification to a specific user identified by their username."""
        if target_username in Notification._user_notifications:
            Notification._user_notifications[target_username].append({"message": message, "is_new": True})
            # print(f"Notification sent to {target_username}.")
        else:
            print(f"User {target_username} does not exist.")

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def view_notifications(self):
        """View and clear notifications for this user."""
        notifications = Notification._user_notifications.get(self.username, [])
        if not notifications:
            print("No notifications to display.")
            return

        print(f"\n--- Notifications for {self.username} ---")
        for i, notification in enumerate(notifications, start=1):
            status = "New" if notification["is_new"] else "Read"
            print(f"{i}. [{status}] {notification['message']}")

        # Mark all notifications as read
        for notification in notifications:
            notification["is_new"] = False

        clear = input("Would you like to clear all notifications? (y/n): ").strip().lower()
        if clear == 'y':
            self.clear_notifications()

    def clear_notifications(self):
        """Clear all notifications for this user."""
        Notification._user_notifications[self.username].clear()
        print("All notifications cleared.")
               
def notify_action(message_template):
    """Decorator to add a notification based on an action."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            # Check if args exist to prevent IndexError
            if args:
                message = message_template.format(*args)
            else:
                message = message_template
            self.notifications.add_notification(message)
            return result
        return wrapper
    return decorator
