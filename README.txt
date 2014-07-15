Name: All mah bits are gone!

Description: ``Some hippy stole all mah bits! It's not a bit if there arn't no
ones! And what's with this here colorful picture. Back in my day, they didn't
have no colorful bits. Just green...'' Can you help Old Man Jenkins find his
bits? He said he had something for you if you did - a relic of the old war, when
he was a standard bearer.

How to Solve: The first thing that should be noticed is that the noise and 
most of the gradients occur in red/green space. Those should be removed, leaving
only the blue layer. In this layer the only addition to the characters is a
smooth gradient. This can be removed via some edge detector (the characters
are high frequency, the gradient is low frequency). This will leave just the
O's and 0's. 

Once those are revealed, it should be noted that the characters are slightly
different in height and width, and are mono-spaced. A grid can be set up across
each of these characters (as they are all uniformly spaced). From there, a 
filter can be run which checks whether a pixel is present (or not), 
discriminating between the two characters. Finally, they can be decoded
via 7-bit ASCII to find a short message, containing the flag.

What to distribute:
dist/challenge.png

Flag:MCA-3F1221C5
