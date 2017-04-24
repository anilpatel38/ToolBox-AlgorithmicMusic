"""Synthesizes a blues solo algorithmically."""

import atexit
import os
import random
# from random import choice

from psonic import *

# The sample directory is relative to this source file's directory.
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

SAMPLE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch


def play_note(note, beats=1, bpm=60, amp=1):
    """Plays note for `beats` beats. Returns when done."""
    # `note` is this many half-steps higher than the sampled note
    half_steps = note - SAMPLE_NOTE
    # An octave higher is twice the frequency. There are twelve half-steps per
    # octave. Ergo,
    # each half step is a twelth root of 2 (in equal temperament).
    rate = (2 ** (1 / 12)) ** half_steps
    assert os.path.exists(SAMPLE_FILE)
    # Turn sample into an absolute path, since Sonic Pi is executing from a
    # different working directory.
    sample(os.path.realpath(SAMPLE_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)


def stop():
    """Stops all tracks."""
    msg = osc_message_builder.OscMessageBuilder(address='/stop-all-jobs')
    msg.add_arg('SONIC_PI_PYTHON')
    msg = msg.build()
    synthServer.client.send(msg)


"""
define a list of lengths for the following function to use.
"""
lengths = []
curr_length = 0.1
for i in range(11):
    lengths.append(curr_length)
    curr_length += 0.03
    curr_length = round(curr_length, 3)


def rand_lick():
    """
    function for making random licks.
    randomizes note length and interval jump
    """
    num_notes = random.choice(range(5, 10))
    notes = []
    for i in range(num_notes):
        interval = random.choice(range(-3, 3))
        length = random.choice(lengths)
        note = (interval, length)
        notes.append(note)
    return notes


# stop all tracks when the program exits normally or is interrupted
atexit.register(stop)

# These are the piano key numbers for a 3-octave blues scale in A.
# See: http://en.wikipedia.org/wiki/Blues_scale
blues_scale = [40, 43, 45, 46, 47, 50, 52, 55, 57, 58, 59, 62, 64, 67, 69, 70,
               71, 74, 76]
beats_per_minute = 45				# Let's make a slow blues solo

r_note = (1, 0.1)       # note in an ascending run lick
r_note2 = (-1, 0.1)     # note in a descending run lick
hold_note = (1, 0.3)    # held out note
length = 0.15           # standard note length for regular licks
curr_note = 0           # starting at curr_note of 0

# pre define two types of lists. Regular swing and a fast run of notes.
straight_lick = [[(1, length * 1.5), (3, length * 0.9), (2, length * 1.5), (-4, length * 0.9)], [(3, length * 1.5), (-2, length * 0.9), (-1, length * 1.5), (3, length * 0.9)]]
run_lick = [[r_note, r_note, r_note, hold_note], [r_note2, r_note2, r_note2, hold_note]]

# run through 8 licks
for _ in range(8):
    """
    To change the frequency of different types of licks I pick a random numbers
    in a range of 0-6 and depending on which number is picked a different list
    of licks is selected from.

    The default swing licks are the most common, random licks are less common,
    and the "runs" are the least common.
    """
    check = random.choice(range(6))
    if check == 4:
        lick = random.choice(run_lick)
        print('run')
    elif check > 4:
        lick = rand_lick()
        # for each random lick start at a random spot not too extreme.
        curr_note = random.choice(range(6, 12))
        print('rand')
    else:
        lick = random.choice(straight_lick)
        print('regular')

    # loop through each note in the licks
    for note in lick:
        curr_note += note[0]
        # print(curr_note)
        # if curr note is out of index then pick a random note near the extreme
        if curr_note > len(blues_scale)-1:
            curr_note = random.choice(range(15, 19))

        # if curr note is out of index then subtract short random interval
        if curr_note < 0:
            curr_note = random.choice(range(1, 6))

        # if statement for making top and bottom of the scale longer notes
        if curr_note == 0 or curr_note == 19:
            play_note(blues_scale[curr_note], 1, beats_per_minute, 1)
        else:
            play_note(blues_scale[curr_note], note[1], beats_per_minute, 1)
