from django import forms
from heydollar.account.models import Account, AccountNameMap

class AccountForm(forms.ModelForm):
    mapped_name = forms.CharField(required=False)
    
    class Meta:
        model = Account
        fields = [
            'description', 'institution', 'type', 'debit_sign', 'owner',
            'login_user', 'login_password',
            'mapped_name',
        ]
        
    def save(self, *args, **kwargs):
        ret = super(AccountForm, self).save(*args, **kwargs)
        return ret
        