from time import strftime

from kivy.animation import Animation
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import get_color_from_hex, Clock
from random import randrange
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

treble_clef_only_L0 = ('C4', 'D4', 'E4', 'F4', 'G4', 'B3', 'A3', 'A4', 'B4', 'C5')
number_of_notes_tcL0 = 10
tcL0_note_img_map = {i: treble_clef_only_L0[i]
                     for i in range(len(treble_clef_only_L0))}

treble_clef_only_L1 = ('D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6', 'B3', 'A3', 'G3')
number_of_notes_tcL1 = 10
tcL1_note_img_map = {i: treble_clef_only_L1[i]
                     for i in range(len(treble_clef_only_L1))}

level_0_notes = (
    'B3B', 'A3B', 'G3B', 'F3B', 'D4B', 'E4B', 'E3B', 'D3B', 'C3B', 'C4B')
number_of_notes_L0 = 10
level_0_note_img_map = {i: level_0_notes[i]
                        for i in range(len(level_0_notes))}

level_1_notes = (
    'B3B', 'A3B', 'G3B', 'F3B', 'D4B', 'E4B', 'E3B', 'D3B', 'C3B', 'C4B', 'B2B', 'A2B', 'G2B', 'F2B', 'E2B', 'D2B', 'C2B', 'B1B', 'A1B')
number_of_notes_L1 = 14
level_1_note_img_map = {i: level_1_notes[i]
                        for i in range(len(level_1_notes))}

level_2_notes = (
    'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6', 'B3', 'A3', 'G3', 'G2B', 'F2B', 'E2B', 'D2B', 'C2B', 'B1B', 'A1B')
number_of_notes_L2 = 17
level_2_note_img_map = {i: level_2_notes[i]
                        for i in range(len(level_2_notes))}


CONST_CLOCK_SCHEDULE_GAME_STATE = 0.5
CONST_TIME_PAUSE_AFTER_QUESTION = 1.5
CONST_TOTAL_NOTES_PER_QUIZ = 10
CONST_TIME_OUT = 7
CONST_END_SCREEN_TIMEOUT = 6

end_screen_timeout = 0
LEVEL = 1
current_note = ""
question_answered = False
question_answered_correct = True
time_out = CONST_TIME_OUT
time_pause_after_question = 3
b_time_pause_after_question = False
score = 0
number_of_correct_res = 0
start_sight_reader = False
played_sound = True  # Setting this to initially false bcos we see the timer going to -0.5 as soon as the game begins.
total_played_questions = 0
number_of_correct_res_bk = 0
b_game_over = False
end_screen_text = ""


def play_sound(filename, button_code='wrong'):
    sound = SoundLoader.load('sounds/' + filename + '.wav')
    sound.play()


class SightReaderButton(Button):
    pass


class SightReaderLayout(GridLayout):
    pass


class MenuLayout(GridLayout):
    def start_sight_reader(self, l):
        global start_sight_reader
        global time_pause_after_question
        global time_out, played_sound, total_played_questions, number_of_correct_res_bk, b_game_over
        global LEVEL, current_note, question_answered, question_answered_correct, b_time_pause_after_question, number_of_correct_res, end_screen_text
        # print(l)
        LEVEL = l
        start_sight_reader = True
        time_out = 0
        time_pause_after_question = 0

        current_note = ""
        question_answered = False
        question_answered_correct = True
        b_time_pause_after_question = False
        number_of_correct_res = 0
        played_sound = True  # Setting this to initially True bcos we see the timer going to -0.5 as soon as the game begins.
        total_played_questions = 0
        number_of_correct_res_bk = 0
        b_game_over = False
        end_screen_text = ""


class PointsWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_points, 0.3)

    def update_points(self, widget, *args):
        self.ids.score.text = "[b]" + str(number_of_correct_res) + "[/b]/" + str(total_played_questions)


class ColorMusicButton(Button):
    pass


class KeyboardNotes(GridLayout):
    def play_sound(self, response_code, button_code='correct'):
        sound = SoundLoader.load('sounds/' + response_code + '.wav')
        sound.play()

    def match_response(self, button_code):
        global question_answered_correct
        global number_of_correct_res
        global score
        global question_answered
        if b_time_pause_after_question == False:
            if button_code[0] == current_note[0]:
                number_of_correct_res += 1
                self.play_sound('correct', button_code[0])
                question_answered_correct = True
            else:
                self.play_sound('wrong', button_code[0])
                question_answered_correct = False

            question_answered = True


class MusicStaffLayout(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Schedule the interval for the animation
        # Clock.schedule_interval(self.animate_it, 1)
        # Clock.schedule_once(self.animate_it, 1)
        self.animate = Animation(
            size_hint=(0.2, 0.2))

        # Do second animation
        self.animate += Animation(
            size_hint=(0.1, 0.1))

        '''animate += Animation(
            size_hint=(0.2, 0.2))
        animate += Animation(
            size_hint=(0.1, 0.1))'''

        Clock.schedule_interval(self.check_game_state, CONST_CLOCK_SCHEDULE_GAME_STATE)

    def check_game_state(self, widget, *args):
        global time_out
        global question_answered

        if start_sight_reader:
            time_out -= CONST_CLOCK_SCHEDULE_GAME_STATE
            # checks if the question is answered or timeout.
            if question_answered or time_out < 1:
                self.show_next_question(widget)
                # time_out = 5
            if b_game_over:
                self.show_game_over()

    def show_next_question(self, widget, *args):
        global question_answered
        global time_pause_after_question
        global time_out
        global b_time_pause_after_question
        global played_sound
        global total_played_questions
        global start_sight_reader
        global number_of_correct_res
        global number_of_correct_res_bk, b_game_over, end_screen_timeout
        global end_screen_text

        b_time_pause_after_question = True
        sw_started = False
        time_pause_after_question -= CONST_CLOCK_SCHEDULE_GAME_STATE

        if question_answered and question_answered_correct:
            self.ids.cta.background_normal = "images/correct.png"
            self.ids.cta.background_down = "images/correct.png"

        elif question_answered and not question_answered_correct:
            self.ids.cta.background_normal = "images/wrong.png"
            self.ids.cta.background_down = "images/wrong.png"

        elif time_out < 1:
            self.ids.cta.background_normal = "images/timeout.png"
            self.ids.cta.background_down = "images/timeout.png"
            if not played_sound:
                play_sound('wrong')
                played_sound = True

        tgt = self.ids.cta
        self.animate.stop(tgt)

        if time_pause_after_question < 1:
            question_answered = False
            b_time_pause_after_question = False
            time_out = CONST_TIME_OUT
            time_pause_after_question = CONST_TIME_PAUSE_AFTER_QUESTION
            img_url = self.get_next_note()
            self.ids.cta.background_normal = img_url
            self.ids.cta.background_down = img_url
            self.animate_it(widget, *args)
            played_sound = False
            total_played_questions += 1
            number_of_correct_res_bk = number_of_correct_res

            if total_played_questions > CONST_TOTAL_NOTES_PER_QUIZ:
                total_played_questions = 0
                number_of_correct_res = 0

                b_game_over = True
                end_screen_timeout = CONST_END_SCREEN_TIMEOUT
                self.ids.cta.background_normal = ''
                self.ids.cta.background_down = ''
                if number_of_correct_res_bk / CONST_TOTAL_NOTES_PER_QUIZ >= 0.8:
                    end_screen_text = 'Good Job! You got ' + str(number_of_correct_res_bk) + '/' + str(
                        CONST_TOTAL_NOTES_PER_QUIZ) + ' correct'
                else:
                    end_screen_text = 'Hmm. You got ' + str(number_of_correct_res_bk) + '/' + str(
                        CONST_TOTAL_NOTES_PER_QUIZ) + ' correct'
        self.ids.cta.text = end_screen_text

    def show_game_over(self):
        global end_screen_timeout, start_sight_reader

        end_screen_timeout -= 1
        if b_game_over and end_screen_timeout < 1:
            start_sight_reader = False
            self.ids.cta.text = ''
            sm.switch_to(MenuScreen(name='menu'))

    def get_next_note(self):
        global current_note

        if LEVEL == 0:
            i = int(randrange(number_of_notes_L0))
            current_note = level_0_note_img_map[i]
            return "images/" + current_note + ".png"
        elif LEVEL == 1:
            i = int(randrange(number_of_notes_L1))
            current_note = level_1_note_img_map[i]
            return "images/" + current_note + ".png"
        elif LEVEL == 2:
            i = int(randrange(number_of_notes_L2))
            current_note = level_2_note_img_map[i]
            return "images/" + current_note + ".png"
        elif LEVEL == 10:  # Treble Clef code BGN =10
            i = int(randrange(number_of_notes_tcL0))
            current_note = tcL0_note_img_map[i]
            return "images/" + current_note + ".png"
        elif LEVEL == 11:  # Treble Clef code BGN =10
            i = int(randrange(number_of_notes_tcL1))
            current_note = tcL1_note_img_map[i]
            return "images/" + current_note + ".png"

    def animate_it(self, widget, *args):
        # Define The Animation you want to do
        # animate = Animation(
        # background_color=(1, 1, 1, 1),
        # duration=1)

        # if time_pause_after_question > 0:
        '''animate = Animation(
            size_hint=(0.2, 0.2))

        # Do second animation
        animate += Animation(
            size_hint=(0.1, 0.1))'''

        '''animate += Animation(
            size_hint=(0.2, 0.2))
        animate += Animation(
            size_hint=(0.1, 0.1))'''

        tgt = self.ids.cta
        self.animate.start(tgt)


class MenuScreen(Screen):
    pass


class SightReaderScreen(Screen):
    pass


class HeaderLayout(GridLayout):
    sw_seconds = 0
    sw_started = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 0)

    def update_time(self, nap):
        if start_sight_reader and not b_game_over:
            if total_played_questions > CONST_TOTAL_NOTES_PER_QUIZ:
                self.ids.header_label.text = 'Your total correct response ' + str(number_of_correct_res) + '/' + str(
                    CONST_TOTAL_NOTES_PER_QUIZ)
            if question_answered or time_out < 1:
                self.stopwatch_reset()
            else:
                if not b_time_pause_after_question:
                    self.sw_seconds += nap
                    minutes, seconds = divmod(self.sw_seconds, 60)
                    # if self.sw_started:
                    '''self.ids.stopwatch.text = (
                                '[size=40][b]%02d[/b][/size].%02d' % (int(seconds), int(seconds * 100 % 100)))'''
                    self.ids.stopwatch.text = (
                            '[size=40][b]%02d[/b][/size]' % (int(seconds)))

        # self.time_prop.text = strftime('[b]%H[/b]:%M:%S')

    def start_stop(self):
        self.root.ids.start_stop.text = ('Start' if self.sw_started else 'Stop')
        self.sw_started = not self.sw_started

    def stopwatch_reset(self):
        # self.sw_started = False
        self.sw_seconds = 0
        self.ids.stopwatch.text = '[size=40][b]00[/b][/size]'

    def back_to_Menu(self):
        global end_screen_text

        global start_sight_reader
        end_screen_text = ""
        start_sight_reader = False


# kv = Builder.load_file("sightreader.kv")

class SightReaderApp(App):
    def build(self):
        self.icon = 'images/icons8-48.png'
        global sm
        # transition=WipeTransition()
        sm = ScreenManager(transition=RiseInTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SightReaderScreen(name='sightreader'))
        # return SightReaderLayout()
        # return kv
        return sm


if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#E4F4F3')
    SightReaderApp().run()
