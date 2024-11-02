from abc import ABC, abstractmethod

class Observer(ABC):
    """Observer interface for all user classes."""
    @abstractmethod
    def update(self, message):
        raise NotImplementedError("Subclasses must implement this method.")
  
class Notification:
    def __init__(self):
        self.notifications = []
        self.observers = []

    def add_observer(self, observer):
        """Register an observer if it’s not already added."""
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            print(f"Observer {observer} is already added.")

    def remove_observer(self, observer):
        """Unregister an observer."""
        self.observers.remove(observer)

    def add_notification(self, message):
        """Add a notification for all observers."""
        self.notifications.append({"message": message, "is_new": True})
        self.notify_observers(message)

    def add_notification_for_observer(self, message, observer):
        """Send a notification to a specific observer."""
        if observer in self.observers:
            observer.update(message)

    def notify_observers(self, message):
        """Notify all observers of the new notification."""
        for observer in self.observers:
            observer.update(message)

    def view_notifications(self):
        """View all notifications, marking them as read after display."""
        if not self.notifications:
            print("No notifications to display.")
            return

        print("\n--- Notifications ---")
        for i, notification in enumerate(self.notifications, start=1):
            status = "New" if notification["is_new"] else "Read"
            print(f"{i}. [{status}] {notification['message']}")

        # Mark all notifications as read
        for notification in self.notifications:
            notification["is_new"] = False

        clear = input("Would you like to clear all notifications? y/n").lower().strip()
        if clear == 'y':
            self.clear_notifications()
   
    def clear_notifications(self):
        """Clear all notifications."""
        self.notifications.clear()
        self.notify_observers("All notifications have been cleared.")
