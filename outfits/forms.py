from django import forms
from .models import Outfit
from closet.models import Clothing

class OutfitForm(forms.ModelForm):
    top = forms.ModelChoiceField(
        queryset=Clothing.objects.none(),  # 初始时为空，将在 __init__ 中设置
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Top"
    )
    bottom = forms.ModelChoiceField(
        queryset=Clothing.objects.none(),  # 初始时为空，将在 __init__ 中设置
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Bottom"
    )
    shoe = forms.ModelChoiceField(
        queryset=Clothing.objects.none(),  # 初始时为空，将在 __init__ 中设置
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Shoe"
    )

    class Meta:
        model = Outfit
        fields = ['name', 'top', 'bottom', 'shoe', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image' 字段如果需要用户上传，则可以在这里定义相应的 widget
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 从视图传递的user参数
        super(OutfitForm, self).__init__(*args, **kwargs)

        # 根据当前用户过滤衣物选项
        if user:
            self.fields['top'].queryset = Clothing.objects.filter(owner=user, type='top')
            self.fields['bottom'].queryset = Clothing.objects.filter(owner=user, type='bottom')
            self.fields['shoe'].queryset = Clothing.objects.filter(owner=user, type='shoe')

        # 如果需要，这里还可以添加其他初始化逻辑

