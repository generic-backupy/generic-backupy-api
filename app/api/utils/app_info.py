class AppInfo:
    def __init__(self, title=None, text=None, icon=None,
                 css_class=None, button_text=None, can_dismiss=None,
                 info_link=None, info_link_text=None, api_link_on_success_button=None,
                 needed_check_box_text=None):
        self.title = title
        self.text = text
        self.icon = icon
        self.css_class = css_class
        self.button_text = button_text
        self.can_dismiss = can_dismiss
        self.info_link = info_link
        self.info_link_text = info_link_text
        self.api_link_on_success_button = api_link_on_success_button
        self.needed_check_box_text = needed_check_box_text

    def get_json(self):
        json = {
            "title": self.title,
            "text": self.text,
            "icon": self.icon,
            "cssClass": self.css_class,
            "buttonText": self.button_text,
            "canDismiss": self.can_dismiss,
            "infoLink": self.info_link,
            "infoLinkText": self.info_link_text,
            "apiLinkOnSuccessButton": self.api_link_on_success_button,
            "neededCheckBoxText": self.needed_check_box_text
        }
        return {k: v for k, v in json.items() if v is not None}

    def append_to(self, appending_json):
        appending_json["appInfo"] = self.get_json()
