// @flow

import { clear, createSvg } from "../utils.js";

/*********/
/* model */
/*********/

export type Notification = {
  text: string,
  inProgress: boolean,
  error: boolean,
  onClick: () => Promise<void>,
  onCloseClick: () => Promise<void>,
};

let model: {
  notificationsOpen: boolean,
  notifications: Array<Notification>,
};

function initModel(): void {
  model = {
    notificationsOpen: false,
    notifications: [],
  };
}

/**********/
/* update */
/**********/

function toggleNotifications(): void {
  model.notificationsOpen = !model.notificationsOpen;
  notificationsView();
}

export function updateNotifications(notifications: Array<Notification>): void {
  model.notifications = notifications;
  notificationsView();
}

/********/
/* view */
/********/

function view(): void {
  notificationsView();
}

function notificationsView(): void {
  const notifications = document.querySelector(".notifications");
  const badge = notifications?.querySelector(".notifications__icon__badge");
  const notificationsList = notifications?.querySelector(
    ".notifications__notifications",
  );

  if (!notifications || !badge || !notificationsList) {
    return;
  }

  const completedNotifications = model.notifications.filter(
    notification => !notification.inProgress,
  );
  if (completedNotifications.length > 0) {
    badge.textContent = completedNotifications.length.toString();
    badge.style.display = "flex";
  } else {
    badge.textContent = "";
    badge.style.display = "none";
  }

  clear(notificationsList);

  if (model.notifications.length) {
    model.notifications.map(function(notification) {
      notificationsList.appendChild(notificationView(notification));
    });
  } else {
    notificationsList.appendChild(noNotificationView());
  }

  if (model.notifications.some(notification => notification.inProgress)) {
    document
      .querySelector(".notifications__spinner")
      ?.classList.add("notifications__spinner--loading");
  } else {
    document
      .querySelector(".notifications__spinner")
      ?.classList.remove("notifications__spinner--loading");
  }

  if (model.notificationsOpen) {
    notifications.classList.add("notifications--open");
  } else {
    notifications.classList.remove("notifications--open");
  }
}

function notificationView(notification: Notification): HTMLDivElement {
  const div = document.createElement("div");
  div.classList.add("notification");
  div.addEventListener("click", notification.onClick);

  if (notification.inProgress) {
    const spinner = document.createElement("loading-spinner");
    spinner.classList.add("notification__spinner");
    div.appendChild(spinner);
  } else {
    let icon;
    if (notification.error) {
      icon = createSvg("error");
      icon.classList.add("notification__icon--error");
      const remove = createSvg("close");
      remove.classList.add("notification__close");
      remove.addEventListener("click", notification.onCloseClick);
      div.appendChild(remove);
    } else {
      div.classList.add("notification--completed");
      icon = createSvg("cloud_download");
    }
    icon.classList.add("notification__icon");
    div.appendChild(icon);
  }

  const description = document.createElement("span");
  description.classList.add("notification__description");
  description.textContent = notification.text;
  div.appendChild(description);

  return div;
}

function noNotificationView(): HTMLDivElement {
  const div = document.createElement("div");
  div.textContent = "No new notifications";
  return div;
}

/*************/
/* listeners */
/*************/

function initEventListeners(): void {
  addNotificationsOpenListener();
}

function addNotificationsOpenListener(): void {
  document
    .querySelector(".notifications")
    ?.addEventListener("click", function(event: MouseEvent) {
      event.stopPropagation();
    });
  document
    .querySelector(".notifications__icon")
    ?.addEventListener("click", function(event: MouseEvent) {
      toggleNotifications();
    });
  document.body?.addEventListener("click", function(event: MouseEvent) {
    if (model.notificationsOpen) {
      event.stopPropagation();
      toggleNotifications();
    }
  });
}

/********/
/* init */
/********/

export function init(): void {
  initModel();
  view();
  initEventListeners();
}