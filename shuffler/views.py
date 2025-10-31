import random
import re
from typing import Any

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import FileForm


class UploadFileView(FormView):
    template_name = "upload_file.html"
    form_class = FileForm
    success_url = "/shuffled-file/"

    def form_valid(self, form: Any) -> HttpResponse:
        content = form.cleaned_data["text_file"]
        delimiters = r"(!|\?|==|\s+|-|\.|\(|\)|\[|\]|\@)"
        shuffled = "".join(
            [self.shuffle_text(word) for word in re.split(delimiters, content)]
        )
        self.request.session["shuffled_content"] = shuffled
        self.request.session["original_text"] = content

        return super().form_valid(form)

    def shuffle_text(self, word: str) -> str:
        """
        Shuffle the inner characters of a word while keeping its first and last characters fixed.

        :param word: string to shuffle content
        :return: shuffled string
        """
        if len(word) < 4:
            return word
        shuffle_content = list(word[1:-1])
        random.shuffle(shuffle_content)
        word = word[0] + "".join(shuffle_content) + word[-1]

        return word


class ShuffledFileView(TemplateView):
    template_name = "view_file.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["shuffled_file"] = self.request.session.pop("shuffled_content", "")
        context["original_text"] = self.request.session.pop("original_text", "")
        return context
