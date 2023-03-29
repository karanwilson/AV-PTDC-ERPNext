from . import __version__ as app_version

app_name = "ptdc_av"
app_title = "Ptdc Av"
app_publisher = "PTDC Labs"
app_description = "Participant Management"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "karanav@vivaldi.net"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ptdc_av/css/ptdc_av.css"
# app_include_js = "/assets/ptdc_av/js/ptdc_av.js"

# include js, css files in header of web template
# web_include_css = "/assets/ptdc_av/css/ptdc_av.css"
# web_include_js = "/assets/ptdc_av/js/ptdc_av.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ptdc_av/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ptdc_av.install.before_install"
# after_install = "ptdc_av.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ptdc_av.uninstall.before_uninstall"
# after_uninstall = "ptdc_av.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ptdc_av.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

doc_events = {
	"Contribution Entry": {
		"after_insert": "ptdc_av.api.add_contribution_payment_entry"
	},
	"Purchase Receipt": {
		"on_submit": "ptdc_av.api.update_selling_price_list",	# creates an 'Item Price' in the 'Selling Price List'
		"before_cancel": "ptdc_av.api.delete_item_price"		# deletes the linked 'Item Price' before cancelling the Purchase Receipt
	},
	"PT Purchase Order": {
		"after_insert": "ptdc_av.api.create_purchase_order"
	},
	"PT Purchase Receipt": {
		"after_insert": "ptdc_av.api.create_purchase_receipt",
	},
	"Container Return": {
		"after_insert": "ptdc_av.api.container_return_credit"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"ptdc_av.tasks.all"
#	],
#	"daily": [
#		"ptdc_av.tasks.daily"
#	],
#	"hourly": [
#		"ptdc_av.tasks.hourly"
#	],
#	"weekly": [
#		"ptdc_av.tasks.weekly"
#	]
#	"monthly": [
#		"ptdc_av.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "ptdc_av.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "ptdc_av.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "ptdc_av.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"ptdc_av.auth.validate"
# ]

