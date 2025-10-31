from io import BytesIO

import pytest


class TestUploadFileView:
    @pytest.mark.django_db
    def test_upload_view_redirects_and_sets_orginal_text_and_shuffled_in_the_session(
        self, client
    ):
        data = {
            "text_file": BytesIO(b"Hello world"),
        }
        response = client.post("/", data, format="multipart")
        assert response.status_code in (302, 303)
        session = client.session
        assert "shuffled_content" in session or "original_text" in session
        assert session.pop("shuffled_content", "") != session.pop(
            "original_content", ""
        )

    @pytest.mark.django_db
    def test_upload_view_correctly_shuffles_text_in_brackets(self, client):
        data = {
            "text_file": BytesIO(b"[Trilo] (Trilo)"),
        }
        _ = client.post("/", data, format="multipart")
        session = client.session
        content = session.pop("shuffled_content", "")
        square_brackets_word = content.split(" ")[0]
        assert square_brackets_word[0] == "["
        assert square_brackets_word[1] == "T"
        assert square_brackets_word[-2] == "o"
        assert square_brackets_word[-1] == "]"

        round_brackets_word = content.split(" ")[-1]
        assert round_brackets_word[0] == "("
        assert round_brackets_word[1] == "T"
        assert round_brackets_word[-2] == "o"
        assert round_brackets_word[-1] == ")"

    @pytest.mark.django_db
    def test_upload_view_correctly_shuffles_emails(self, client):
        data = {
            "text_file": BytesIO(b"example@email"),
        }
        _ = client.post("/", data, format="multipart")
        session = client.session
        content = session.pop("shuffled_content", "")

        assert content.split("@")[0][0] == "e"
        assert content.split("@")[0][-1] == "e"

        assert content.split("@")[-1][0] == "e"
        assert content.split("@")[-1][-1] == "l"

    @pytest.mark.django_db
    def test_upload_view_correctly_shuffles_websites(self, client):
        data = {
            "text_file": BytesIO(b"www.example.com"),
        }
        _ = client.post("/", data, format="multipart")
        session = client.session
        content = session.pop("shuffled_content", "")

        assert len(content.split(".")[0]) == 3
        assert len(content.split(".")[1]) == 7
        assert content.split(".")[1][0] == "e"
        assert content.split(".")[1][-1] == "e"
