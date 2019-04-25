from django.db import models
from core.models import Core, Country, State, City
from django_resized import ResizedImageField


class ContentProvider(Core):
    """
    Content Provider
    """
    name = models.CharField("Provider Name", max_length=255)
    url = models.URLField("Provider Link", blank=True, null=True)

    def __str__(self):
        return self.name


class AssetType(Core):
    """
    Types of assets
    """
    name = models.CharField("Asset Type", max_length=20)

    def __str__(self):
        return self.name


class AssetContent(Core):
    """
    Content in assets
    """
    identifier = models.CharField("Identifier", max_length=255)
    content = models.FileField("Asset Content", upload_to="uploads", blank=True, null=True, help_text="Video supported .mp4, .avi and .webm")
    alternate_text = models.CharField("alternate_text", max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    start_time = models.IntegerField(default=0, help_text="In seconds not decimal values")
    duration = models.IntegerField(default=5, help_text="In seconds ")


class Asset(Core):
    """
    Asset related to content
    """
    name = models.CharField("Identifier", max_length=255)
    asset_type = models.ForeignKey(AssetType, blank=True, null=True, on_delete=models.DO_NOTHING)
    asset_content = models.ManyToManyField(AssetContent, blank=True, related_name="asset_contents")
    source = models.CharField(max_length=255, blank=True, null=True)
    content_attribution = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = ResizedImageField(size=[300, 180], crop=['middle', 'center'], upload_to='uploads/thumbnails/', blank=True, null=True)


class AssetAssociation(Core):
    """
    Asset Association with template location
    """
    asset = models.ForeignKey(Asset, blank=True, null=True, related_name="asset_assocaition", on_delete=models.DO_NOTHING)
    template_location = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.template_location:
            return "At "+self.template_location+" asset "+self.asset.name
        else:
            return self.asset.name


class Partner(Core):
    """
    Partners Model
    """
    name = models.CharField(max_length=100, help_text="Partner Name")
    logo = models.URLField(blank=True, null=True, help_text="Partner Logo")
    description = models.TextField(blank=True, help_text="Partner Description")

    def __str__(self):
        return self.name


class AdSection(Core):
    """
    Ad information container
    """
    name = models.CharField("Ad Name",  max_length=255)
    script = models.TextField("Ad Script", blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Campaign(Core):
    """
    Campaigns Model
    """
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Sponsor(Core):
    """
    Sponsors models
    """
    name = models.CharField(max_length=255)
    logo  = models.FileField(upload_to='uploads/sponsors/',blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class TemplateContent(Core):
    """
    Content according to template
    """

    class Meta:
        verbose_name = "Content For Template"   # For django admin

    TEMPLATE_CHOICE = (
        ("Editorial Template", "Editorial Template"),
        ("Vehicle Editorial Template", "Vehicle Editorial Template"),
    )

    # Article Details
    content_heading = models.CharField("Article Heading", max_length=255, help_text="Heading of Article")
    content_subheading = models.CharField("Article Sub Heading", max_length=255, blank=True, help_text="SubHeading of Article")
    content_url = models.URLField("External URL", default="http://bainslabs.in", blank=True, help_text="External Url")
    content_byline = models.TextField("Article Byline", default="Byline Goes here", blank=True)
    content_byline_link = models.TextField("Article Byline Link", default="http://bainslabs.in/", blank=True)
    content_body = models.TextField("Article Body", default="article body", blank=True, help_text="Article Body")
    content_synopsis = models.TextField("Article Synopsis", default="article synopsis", blank=True, null=True, help_text="Synopsis")
    content_publish_date = models.DateTimeField("Article Publish Date", auto_now_add=True, help_text="Content Publish Date")
    secondary_navigation = models.ManyToManyField('self', blank=True, related_name="secondary_related_articles", symmetrical=False, help_text="Secondary Navigation")
    related_articles = models.ManyToManyField('self', blank=True, related_name="article_similar", symmetrical=False, help_text="Similar Articles")
    content_provider = models.ForeignKey(ContentProvider, blank=True, null=True, related_name="provided_by", on_delete=models.DO_NOTHING, help_text="Content Provider")
    asset_template_association = models.ManyToManyField(AssetAssociation, related_name="associated_asset", blank=True, help_text="Asset Template Association")
    # Advertisements
    related_ads = models.ManyToManyField(AdSection, related_name="ads_related", blank=True)
    disable_ads = models.BooleanField(default=False)

    # Article Source
    content_partners = models.ForeignKey(Partner, blank=True, null=True, on_delete=models.DO_NOTHING, help_text="Content Partner")
    content_received_date = models.DateTimeField("Article Received Date ", blank=True, null=True, help_text="Content Received Date")
    # Search Area
    search_keywords = models.TextField("Search Keywords", blank=True, null=True, help_text="Search Keywords")
    search_boost = models.IntegerField(default=0, blank=True, null=True, help_text="Search Boost")
    include_in_search = models.BooleanField(default=False, help_text="Searchable")
    # SEO Related Fields
    guid = models.CharField("Canonical Link", max_length=255, blank=True, null=True, help_text="Canonical Link")
    seo_meta_name = models.CharField("Seo Meta Name", max_length=100, blank=True, null=True, help_text="SEO Meta Information")
    seo_keywords = models.TextField("Seo Keyword", blank=True, null=True, help_text="SEO Keywords")
    seo_meta_description = models.TextField("Meta Description", blank=True, null=True, help_text="SEO Description")
    # Template Choiceasset_content.to_json
    template = models.CharField(max_length=255, choices=TEMPLATE_CHOICE, default="", blank=True, null=True, help_text="Template type")
    preview_path = models.CharField(max_length=20, blank=True, null=True)
    # Article Tagging
    country = models.ForeignKey(Country, related_name="countries_available", blank=True, null=True, on_delete=models.DO_NOTHING, help_text="Country")
    state = models.ForeignKey(State, related_name="states_available", blank=True, null=True, on_delete=models.DO_NOTHING, help_text="State")
    city = models.ForeignKey(City, related_name="cities_available", blank=True, null=True, on_delete=models.DO_NOTHING, help_text="City")
    sponsor = models.ForeignKey(Sponsor, blank=True, null=True, on_delete=models.DO_NOTHING, help_text="Sponsor")
    is_timely_content = models.BooleanField("Timely Content",default=False, help_text="Expirable Content")
    available_in_trends = models.BooleanField("Available In Trends",default=False, help_text="Available in Trends")
    disable_personalization = models.BooleanField("Disable Personalisation", default=False, help_text="Disable Personalization")
    is_promoted_content = models.BooleanField("Promoted Content", default=False, help_text="Promoted Content")
    homepage_availability = models.BooleanField("Available On Homepage", default=False, help_text="Is Available on Homepage")
    campaign = models.ManyToManyField(Campaign, related_name="campaign_related", blank=True)
    year = models.IntegerField("Year",blank=True, null=True, help_text="Year")
    manufacturer = models.TextField("Manufacturer", blank=True, null=True, help_text="Manufacturer")
    make = models.TextField("Make", blank=True, null=True, help_text="Make")
    make_model = models.TextField("Make model", blank=True, null=True, help_text="Model Make")
    likes = models.IntegerField("likes", default=0, blank=True, null=True, help_text="Likes")
    views = models.IntegerField("views", default=0, blank=True, null=True, help_text="Views")
    slug = models.SlugField("slug", max_length=255, blank=True, null=True, help_text="Unique Slug")
    is_featured = models.BooleanField("Is Featured", default=False, help_text="Is Featured")

    # Configuration
    template_configuration = models.TextField("Template Configuration", blank=True, null=True, help_text="Template Configuration")



    def __str__(self):
        return self.content_heading if self.content_heading else "Content "+str(self.id)


class PublishingState(Core):
    """
    publishing state and publish restrictions of any content
    """
    publish_state_choices = (
        ("Draft","Draft"),
        ("Ready To Approve", "Ready To Approve"),
        ("Published","Published"),
    )

    content = models.OneToOneField(TemplateContent, on_delete=models.DO_NOTHING)
    publish_state = models.CharField(max_length=20, choices=publish_state_choices, blank=True, null=True)
    unpublishing_on = models.DateTimeField(blank=True, null=True)
    do_not_publish_until = models.DateTimeField("Do Not Publish Until", blank=True, null=True)
    not_for_external_use = models.BooleanField("Not For External Use", default=False)


    def __str__(self):
        return self.content.content_heading
