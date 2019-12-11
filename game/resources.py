from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field

from .models import Question, Option

class QuestionResource(resources.ModelResource):
    option0 = fields.Field(column_name='選項一')
    option1 = fields.Field(column_name='選項二')
    option2 = fields.Field(column_name='選項三')
    option3 = fields.Field(column_name='選項四')
    answer = fields.Field(column_name='答案')
    topic = Field(attribute='topic', column_name='題目')
    solution = Field(attribute='solution', column_name='詳解')
    
    class Meta:
        model = Question
        fields = ('topic', 'solution', 'option0', 'option1', 'option2', 'option3', 'answer') #顯示的欄位
        export_order = ('topic', 'solution', 'option0', 'option1', 'option2', 'option3', 'answer') #顯示順序
    
    def dehydrate_option0(self, question):
        return '%s' % (question.options.all()[0].description)
    
    def dehydrate_option1(self, question):
        return '%s' % (question.options.all()[1].description)
    
    def dehydrate_option2(self, question):
        return '%s' % (question.options.all()[2].description)
    
    def dehydrate_option3(self, question):
        return '%s' % (question.options.all()[3].description)
    
    def dehydrate_answer(self, question):
        return '%s' % (question.options.filter(score=1).first().description)
