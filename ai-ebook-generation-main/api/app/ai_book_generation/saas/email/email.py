class EmailTemplate:
    @staticmethod
    def get_subject(title):
        return f"Your AI-Generated eBook '{title}' is Ready for Download"

    @staticmethod
    def get_body(title, topic, target_audience, file_url, id, recipient_email, docx_url=False):
        message = f"""
Hi,

We are excited to inform you that your AI-generated eBook is now ready for download. Here are the details:

Title: {title}
Topic: {topic}
Reader: {target_audience}
Id: {id}
Email: {recipient_email}

View your full E-Book here:
{file_url}
"""

        if docx_url:
            message += f"""
View the docx here (Note that this will fail to load in browser - Use Right-Click -> "Save As" to save the docx file):
{docx_url}
"""
        message += f"""
We hope you enjoy reading your AI-generated eBook. If you have any questions or need further assistance, please do not hesitate to contact us.

Thank you for choosing our AI eBook Generation Service.
"""

        return message
