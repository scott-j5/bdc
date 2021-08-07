from django.db import models

# Create your models here.
class PriceAdjustment(models.Model):
	ADJ_TYPES = [('PER', '%'), ('DOL', '$')]
	slug = models.SlugField(blank=True, null=False)
	name = models.CharField(max_length=50, blank=False, null=False)
	description = models.TextField(null=True, blank=True)
	period_start = models.DateTimeField(blank=False, null=False)
	period_end = models.DateTimeField(blank=False, null=False)
	adj_type = models.CharField(max_length=3, choices=ADJ_TYPES, default='PER', blank=False, null=False)
	adj_amount = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return f"{self.name} - ({self.adj_amount}{self.adj_type}) Valid:{self.period_start}-{self.period_end}"

	@property
	def amount_humanize_long(self):
		if self.adj_amount < 0:
			adj_value = str(self.adj_amount).strip("-")
			human_type = "off"
		else:
			adj_value = str(self.adj_amount)
			human_type = "increase"
		return f"{self.name} - {adj_value}% {human_type}" if self.adj_type == "PER" else f"{self.name} - ${adj_value} {human_type}"


	@property
	def amount_humanize(self):
		if self.adj_amount < 0:
			adj_value = str(self.adj_amount).strip("-")
			human_type = "-"
		else:
			adj_value = str(self.adj_amount)
			human_type = "+"
		return f"{human_type} {adj_value}%" if self.adj_type == "PER" else f"{human_type} ${adj_value}"

	def clean(self):
		if not self.slug or self.slug == '':
			self.slug = self.name.replace(' ', '-').lower()