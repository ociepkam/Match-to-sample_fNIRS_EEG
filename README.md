# Match-to-sample_fNIRS_EEG
Match-to-sample task modified for the fNIRS-EEG measurement.

Each of 72 trials consists of presentation of a central shape, together with the cluster of 3-8 (factor: load) unique shapes presented either to the left or to the right (factor: hemifield) of the central shape (12 conditions in total, 6 trials each) for 5 s. In each condition, in 3 trials the central shape is also present in the cluster, while in the remaining 3 trials it is absent (factor: match). The central and the cluster shapes have their unique colors (red, white, blue, red, green, yellow, brown, violet, pink). The task is to press (within 5 s) one key when the central shape and one of the cluster shapes match and another key when no shape matches. Each trial is followed by a jittered pause presenting a fixation cross centrally for 8-12 s. A 20-s fixation dot precedes the first trial. The total duration of the task is 18 minutes. We will try to calculate within-participant correlation across 24 data points (6 loads x 2 hemifields x 2 match), or at least across 12 data points (collapsed over the match factor). 

Triggers:
* 1<trial number> - fixation point 
* 2<trial number> - stimulus 
* 3<trial number> - participant response