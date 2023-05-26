from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random
import json
from functools import reduce
import csv
import datetime


author = 'Ty Hayes'

doc = """
oTree wrapper for a dice rolling experiment
that makes use of mobile phone's accelerometer
to detect the motion of the participant's hands.
"""


class Constants(BaseConstants):
    name_in_url = 'dice_rolling'
    players_per_group = None
    trials_per_target = 4
    num_rounds = trials_per_target*6
    output_path = "/your/data/dir"  #path to output data serverside (due to large filesize, streaming HTTP response may time out)
    experimenter_prolific_id = "YOUR_PROLIFIC_PID" #experimenter prolific ID for automatic exclusion


class Subsession(BaseSubsession):
    def creating_session(self):
        '''
        Populates targets and results fields on creating sesion
        Targets populated as blocks of {Constants.trials_per_target}
        trials, results uniformly randomly
        '''
        for p in self.get_players():
            if self.round_number == 1:
                target_order = list(range(1,7))
                random.shuffle(target_order)
                p.participant.vars['target_order'] = target_order
                p.participant.save()
                print(p.participant.vars)
            p.target = p.participant.vars['target_order'][(self.round_number -1)//Constants.trials_per_target]
            p.result = random.randint(1,6)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    target = models.IntegerField(min=1, max=6)  # the number the participants has to roll for a bonus
    result = models.IntegerField(min=1, max=6)  # (pseudo)randomly determined outcome for the trial
    accelerometer_data = models.TextField(max_length=None) # json array of objects.  each object
                                                           # contains x, y, z readings from the accelerometer
                                                           # on participants device (passed from javascript task
                                                           # code), and an extra key, w, as the magnitude 
                                                           # of the vector
    errors = models.TextField(max_length=None, default="") # json array of strings. any javascript exceptions
                                                           # caught by the task on this particular trial are saved here
    final_die_z = models.StringField(blank=True)           # final position of the die on the world z axis 
                                                           # (proportional to distance from backboard
                                                           # of digital dice table).  Not probative in this
                                                           # version of the task
    animation = models.TextField(max_length=None, blank=True) # animation frame data for the die release animation. 
                                                              # Not probative in this version of the task  with
                                                              # pre-recorded animations


    def live_method(self, data):
        '''
        if data.type is acc_data:
          receives and saves accelerometer data from the phone and returns the
          randomly determined result (see Subsession.creating_session())
        
        if type is error:
          adds the current error description to the list of errors 
          (no return message)
        '''
        if data['type'] == "acc_data":
            self.accelerometer_data = json.dumps(data["payload"])
            return {0: self.result}
        elif data['type'] == "error":
            print(data)
            self.errors += f"[{data['payload']}],"

    def set_payoff(self):
        '''
        set bonus value if target = result
        '''
        if self.target == self.result:
            self.payoff = c(1)

def custom_export(players):
    header = ['participant_code', 'target', 'result', 'payoff', 'accelerometer_data', 'mean_abs_magnitude', 'errors','trial_no']
    yield header
    for p in players:
        if p.participant._index_in_pages < p.participant._max_page_index:
            print("skipping participant that did not finish")
            continue #participant did not finish the experiment
        acc_data_json = json.loads(p.accelerometer_data)
        mean_abs_magnitude = reduce(lambda val, x: val + float(x['w']), acc_data_json, 0)/len(acc_data_json) #w is absolute magnitude calculated by the javascript while the task is running
        acc_data_json = [{'x': float(a['x']), 'y': float(a['y']), 'z': float(a['z'])} for a in acc_data_json] # remove the 'w' keys
        yield [p.participant.code, p.target, p.result, p.payoff, acc_data_json, mean_abs_magnitude, p.errors, p.trial_no]

def serverside_custom_export(players=[]):
    '''
    due to large file size and complex data, the standard export may time out during a streaming response
    this will generate the file asynchronously and save it in Constants.data_dir on your server
    '''
    header = ['participant_code', 'target', 'result', 'payoff', 'accelerometer_data', 'mean_abs_magnitude', 'errors','trial_no']
    if not players:
        players = Player.objects.all()
    with open(f'{Constants.data_dir}/dice_rolling_data_{datetime.datetime.now().replace(microsecond=0).isoformat().replace(":", "")}.csv', "w") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for p in players:
            try:
                if p.participant._index_in_pages < p.participant._max_page_index:
                    print("skipping participant that did not finish")
                    continue #participant did not finish the experiment
                if p.participant.label == Constants.experimenter_prolific_id: # remove experimenter's prolific ID
                    continue
                acc_data_json = json.loads(p.accelerometer_data)
                mean_abs_magnitude = reduce(lambda val, x: val + float(x['w']), acc_data_json, 0)/len(acc_data_json) #w is absolute magnitude calculated by the javascript while the task is running
                acc_data_json = [{'x': float(a['x']), 'y': float(a['y']), 'z': float(a['z'])} for a in acc_data_json] # remove the 'w' keys
                writer.writerow([p.participant.code, p.target, p.result, p.payoff, acc_data_json, mean_abs_magnitude, p.errors, p.round_number])
            except Exception as e:
                print(f"problem with participant code {p.participant.code}: {e.__repr__()}")
    print("Done writing")

def serverside_custom_export_with_final_z(players=[]):
    '''
    due to large file size and complex data, the standard export may time out during a streaming response
    this will generate the file asynchronously and save it in Constants.data_dir on your server
    '''
    header = ['participant_code', 'target', 'result', 'payoff', 'accelerometer_data', 'mean_abs_magnitude', 'errors', 'final_die_z', 'trail_no']
    if not players:
        players = Player.objects.all()
    with open(f'{Constants.data_dir}/dice_rolling_data_{datetime.datetime.now().replace(microsecond=0).isoformat().replace(":", "")}.csv', "w") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for p in players:
            try:
                if p.participant._index_in_pages < p.participant._max_page_index:
                    print("skipping participant that did not finish - assumed to be withdrawal")
                    continue #participant did not finish the experiment
                if p.participant.label == Constants.experimenter_prolific_id: # remove experimenter's prolific ID
                    continue
                acc_data_json = json.loads(p.accelerometer_data)
                mean_abs_magnitude = reduce(lambda val, x: val + float(x['w']), acc_data_json, 0)/len(acc_data_json) #w is absolute magnitude calculated by the javascript while the task is running
                acc_data_json = [{'x': float(a['x']), 'y': float(a['y']), 'z': float(a['z'])} for a in acc_data_json] # remove the 'w' keys
                writer.writerow([p.participant.code, p.target, p.result, p.payoff, acc_data_json, mean_abs_magnitude, p.errors, p.final_die_z, p.round_number])
            except Exception as e:
                print(f"problem with participant code {p.participant.code}: {e.__repr__()}")
    print("Done writing")
