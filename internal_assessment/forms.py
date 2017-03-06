from django import forms


class MetricForm(forms.Form):
    """
    This form is used to change or add metrics to a subject in the
    edit-metrics view. It is not bound to the Metric model directly.
    """
    metric_name = forms.CharField(max_length=20)
    max_marks = forms.IntegerField(min_value=0)
