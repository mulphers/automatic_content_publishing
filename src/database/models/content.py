from odmantic import Field, Model


class Content(Model):
    content_id: int = Field(
        primary_field=True,
        index=True,
        unique=True
    )
    url: str
    description: str = Field(default='')
