
# Source: https://github.com/kivy/kivy/wiki/Editable-Label

from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty

from modeful.ui.base.alignedtextinput import AlignedTextInput

__all__ = ('EditableLabel', )

class EditableLabel(Label):

    edit = BooleanProperty(False)
    prev_text = StringProperty('')
    multiline = BooleanProperty(False)

    textinput = ObjectProperty(None, allownone=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.bind(size=self.on_size)

    def on_size(self, *_):
        self.text_size = self.size


    def on_touch_down(self, touch):
        if touch.is_double_tap and self.collide_point(*touch.pos) and not self.edit:
            self.edit = True
            return True
        else:
            return super().on_touch_down(touch)
        
    def on_edit(self, instance, value):
        if not value:
            if self.textinput:
                self.remove_widget(self.textinput)
            return
        self.textinput = t = AlignedTextInput(
                text=self.text, size_hint=(None, None),
                font_size=self.font_size, font_name=self.font_name,
                pos=self.pos, size=self.size, multiline=self.multiline,
                background_color=(1, 1, 1, 0),
                halign=self.halign, valign=self.valign)
        self.bind(pos=t.setter('pos'), size=t.setter('size'))
        self.add_widget(self.textinput)
        self.prev_text = self.text
        self.text = ''
        t.bind(on_text_validate=self.on_text_validate, focus=self.on_text_focus)
        
        Clock.schedule_once(self._do_focus_textinput)

    def on_text_validate(self, instance):
        self.text = instance.text
        self.edit = False

    def on_text_focus(self, instance, focus):
        if focus is False:
            self.text = instance.text
            self.edit = False

    def _do_focus_textinput(self, *largs):
        self.textinput.focus = True
        


