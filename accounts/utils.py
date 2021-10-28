import datetime

def user_display_name(user):
	return user.profile.display_name


def user_display_name_with_date(user):
	return f'{user.profile.display_name} (Created: {user.date_joined.strftime("%d/%m/%Y %H:%M %Z")})'