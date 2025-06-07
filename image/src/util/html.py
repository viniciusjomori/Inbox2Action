def create_task_table(
    id,
    name,
    priority,
    due_date,
    list_name,
    description,
    tokens
):
    return f"""<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; font-family: Arial, sans-serif; padding: 24px;">
    <tr>
        <td style="padding: 24px;">
            <h2 style="color: #2c3e50; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px; margin: 0;">
            Tarefa <i>#{id}</i> criada com sucesso
            </h2>
            <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; width: 30%; vertical-align: middle;">Nome</td>
                    <td style="padding: 8px 0; vertical-align: middle;">{name}</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="padding: 8px 0; font-weight: bold; vertical-align: middle;">Prioridade</td>
                    <td style="padding: 8px 0; vertical-align: middle;">{priority}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; vertical-align: middle;">Prazo</td>
                    <td style="padding: 8px 0; vertical-align: middle;">{due_date.strftime('%d/%m/%Y')}</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="padding: 8px 0; font-weight: bold; vertical-align: middle;">Lista</td>
                    <td style="padding: 8px 0; vertical-align: middle;">{list_name}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; vertical-align: middle;">Descrição</td>
                    <td style="padding: 8px 0; vertical-align: middle;">{description}</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="padding: 8px 0; font-weight: bold; vertical-align: middle;">Tokens</td>
                    <td style="padding: 8px 0; vertical-align: middle;">{tokens}</td>
                </tr>
            </table>
        </td>
    </tr>
</table>
"""