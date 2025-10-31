from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat


class FileForm(forms.Form):
    text_file = forms.FileField()

    def clean_text_file(self) -> str:
        uploaded_file = self.cleaned_data.get("text_file")
        if not uploaded_file:
            return ""
        max_upload_size = settings.FILE_UPLOAD_MAX_MEMORY_SIZE

        if uploaded_file.size > max_upload_size:
            raise ValidationError(
                (
                    f"File size {filesizeformat(uploaded_file.size)}"
                    f" exceeds the maximum allowed {filesizeformat(max_upload_size)}."
                ),
            )

        try:
            content_bytes = uploaded_file.read()
        except Exception as e:
            raise ValidationError(f"Could not read or process file: {e}")

        try:
            charset = getattr(uploaded_file, "charset", "utf-8") or "utf-8"
            content = content_bytes.decode(charset)
        except Exception:
            content = content_bytes.decode("utf-8", errors="replace")

        return content
