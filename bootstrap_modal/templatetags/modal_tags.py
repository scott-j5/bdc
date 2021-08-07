from django import template
#from django.template.library import parse_bits
from django.template.base import token_kwargs
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

register = template.Library()


def evaluate_filter_expr(filter_expr, context):
	var = filter_expr.var if hasattr(filter_expr, 'var') else filter_expr
	if type(var) is template.Variable:
		var = var.resolve(context)
	return var


# Generate a random id for instances where target_modal is not specified
def get_random_modal_uuid():
	uid = get_random_string(6)
	return f"django-bs5-modal-{ uid }"


# Take a parser and whole token and return all the kwargs
# Will not work for partial tokens or tokens with some positional args
def parse_args(parser, token):
	try:
		bits = token.split_contents()
		# Parse optional params for conversion to args, kwargs
		args = bits[1:]
		parsed = token_kwargs(args, parser)
		return parsed
	except ValueError:
		raise template.TemplateSyntaxError(
			"There was an error parsing arguments to the %r tag" % bits[0]
		)


# Creates a modal with a given id
@register.simple_tag(name="modal")
def modal(target_modal, *args, **kwargs):
	context = {
		"target_modal": target_modal,
	}
	return render_to_string('bootstrap_modal/modal.html', context)

# Creates a modal with a given id
def modal_wrapper(parser, token):
	tag_name, format_string = token.split_contents()
	extra_context = {
			"target": format_string[1:-1],
	}
	nodelist = parser.parse(('end_modal_wrapper',))
	parser.delete_first_token()
	return ModalWrapperNode(nodelist, **extra_context)


# Creates a modal button that will open the content within the specified modal
def modal_btn(parser, token):
	return ModalBtnNode(**parse_args(parser, token))


# Creates a modal link that will open the content within the specified modal
def modal_link(parser, token):
	return ModalLinkNode(**parse_args(parser, token))

# Wraps containing text in a link that will open the content within a modal
def modal_link_wrapper(parser, token):
	extra_context = parse_args(parser, token)
	nodelist = parser.parse(('end_modal_link_wrapper',))
	parser.delete_first_token()
	return ModalLinkWrapperNode(nodelist, **extra_context)


class GenericModalNode(template.Node):
	def __init__(self, *args, **kwargs):
		self.target_modal = kwargs.get("target", get_random_modal_uuid())
		self.url = kwargs.get("url", "#")
		self.prompt_text = kwargs.get("prompt_text", "Default Text")
		self.class_list = kwargs.get("class_list", "btn btn-primary")
		self.extra_context = kwargs

	def render(self, context, extra_context={}):
		#try:
		#if not (self.url[0] == self.url[-1] and self.url[0] in ('"', "'")):
			# If url is parsed as an object property, fetch it
		#self.url = template.Variable(self.url.Template)
		#self.url = self.url.resolve(context)
		#except template.VariableDoesNotExist:
		#	return f'Tag error {self.url}'
		
		extra_context.update({
			"target_modal": evaluate_filter_expr(self.target_modal, context),
			"url" : evaluate_filter_expr(self.url, context),
			"prompt_text": evaluate_filter_expr(self.prompt_text, context),
			"class_list": evaluate_filter_expr(self.class_list, context),
		})
		return render_to_string(self.template_name, extra_context)

class ModalBtnNode(GenericModalNode):
	template_name = 'bootstrap_modal/modal_btn.html'

	def __init__(self, *args, **kwargs):
		prompt_text = kwargs.pop("btn_text", "Modal Button")
		super().__init__(*args, **kwargs, prompt_text=prompt_text)


class ModalLinkNode(GenericModalNode):
	template_name = 'bootstrap_modal/modal_link.html'

	def __init__(self, *args, **kwargs):
		prompt_text = kwargs.pop("link_text", "Modal Link")
		class_list = kwargs.pop("class_list", "btn btn-link")
		super().__init__(*args, **kwargs, prompt_text=prompt_text, class_list=class_list)


class ModalWrapperNode(GenericModalNode):
	template_name = 'bootstrap_modal/modal.html'

	def __init__(self, nodelist, *args, **kwargs):
		self.nodelist = nodelist
		super().__init__(*args, **kwargs)

	def render(self, context):
		extra_context = {
			"node_content" : self.nodelist.render(context)
		}
		return super().render(context, extra_context)


class ModalLinkWrapperNode(GenericModalNode):
	template_name = 'bootstrap_modal/modal_link_wrapper.html'

	def __init__(self, nodelist, *args, **kwargs):
		self.nodelist = nodelist
		super().__init__(*args, **kwargs)

	def render(self, context):
		extra_context = {
			"node_content" : self.nodelist.render(context)
		}
		return super().render(context, extra_context)


register.tag('modal_btn', modal_btn)
register.tag('modal_link', modal_link)
register.tag('modal_wrapper', modal_wrapper)
register.tag('modal_link_wrapper', modal_link_wrapper)