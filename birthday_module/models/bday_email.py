from odoo import models,fields,api
from datetime import datetime

class BdayEmail(models.Model):
    _name = "bday.email"
    _description = "Birthday Email Wishes"

    def _bday_email_wishes(self):
        print("Happy Birthday")
        today = datetime.today().strftime('%m-%d')  # Get today's month and day
        partners = self.env['res.partner'].search([])
        print(today)
        print(partners)
        for partner in partners:    
            if partner.birthday:
                print(partner.birthday)
                birthday_date = partner.birthday.strftime('%m-%d')  # Extract month and day
                if birthday_date == today:
                    print("Match date : ",birthday_date == today)
                    self._send_birthday_email(partner)
                    

    def _send_birthday_email(self, partner):
            mail_template = self.env.ref('birthday_module.email_template_birthday_wishes') 
            print("Function is Called") # Ensure XML template exists
            if mail_template:
                mail_template.sudo().send_mail(partner.id, force_send=True)






















# self._send_birthday_email(partner)
    