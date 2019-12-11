from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field

from .models import Question

class QuestionResource(resources.ModelResource):
    topic = Field(attribute='topic', column_name='題目')
    solution = Field(attribute='solution', column_name='詳解')
    option_1 = fields.Field(attribute='option_1', column_name='選項一')
    option_2 = fields.Field(attribute='option_2', column_name='選項二')
    option_3 = fields.Field(attribute='option_3', column_name='選項三')
    option_4 = fields.Field(attribute='option_4', column_name='選項四')
    correct_option = fields.Field(attribute='correct_option', column_name='答案')
    
    class Meta:
        model = Question
        fields = ('topic', 'solution', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option') #顯示的欄位
        export_order = ('topic', 'solution', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option') #顯示順序
