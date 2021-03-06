from kivy.gesture import GestureDatabase, Gesture
#from kivy.metrics import Metrics

def distance():
	#Metrics.dpi() returns the dpi of the screen. 
	#Use this to convert the pixle distance to a 
	#real distance the can work on all sizes of screen.
	pass

def simplegesture(name, point_list):
	g = Gesture()
	g.add_stroke(point_list)
	g.normalize()
	g.name = name
	return g

gdb = GestureDatabase()

swipe_right = gdb.str_to_gesture(b'eNp91FtIFFEYB/BZL2te8lKmXay2NB211MrKstrJLsfsombamK6urpOzrrr7rbuV0AfrSxpkgQ+iBeWDDwkRPgQVPShBYVAioaBFYBTUS1gvPfhQnT2uYXNkzsPMx39+33yHgTm+YJvDfrk9q1Fp83jdSgQJ3EFI7wADQpAohwqCcMXe4FEhmEiVPsG/ZCO9qIq9UfVACJGEhSXH0EvgTbUut7PBa/NAKJHCHA/nrT/vymH0cZvH7XQobWC0QNiyo8sYiIAVdAPhCBEim+Vy2ls9bRBpgShx2bYSP4iAlbQrGiFGlA206yrEkpHPHQ7RapxnQTvEEbOvN3V6Lkfw1qt+vQphtahS92lupnfcq6pxZKRqzj6TZloU8QhrmJh91FfenZvKiwSERCY+9jd/rRjs4sVahHX6Yj3CBiZmpoaSe2bHeJGEsFFfbELYzMRkTjB+zzfxwoSwRV9sRUjWFykI25h4G/98+HamwItUhDR9ISKk64sMhEwmRruyU4LuuXixHWGHvshCyNYXOQg7mejsMRTn/VpmH7sQduuLXIQ9+mIvwj6/MD8dqoLH12Z5kYewX18cQMjXFwcRDumLwwhmJl7VPHnxpdDHCwnhiL4oQDjKxJvB3+EZt0Z5cQzhuL44gUCYmJgydCa+/saLQoSTTLxLKBirjBR5UYRwionJvpdFH7of8OI0whkmpt4bbyaNLzPlLEIxE9PVN6Lvl/7/7ytylP+8srkVpTVw/JRYoFQkUqOVHXdEgoXiOpyj4YA2LCOSKiyGJYHwPA192rCcSHZJG1YQqYlrv0Akh0kbykRqNv/xryVhJZFauEEXieTk3llFJFeONqym4bA2tNCaa6+hNbf52n/fYUlopTW3pTpaD2jDelpz0220HtWGDbSe0IYKrX9ow0tEcnObb6Rh7GLoCoSq4q2vk8Np7XE2K+66VpsCdmJ+1u9fd+QQ+qC1rkWBJtnvweGtz/oLfF9bqw==')

swipe_left = gdb.str_to_gesture(b'eNp91HtQVFUcwPGLgrCIj6TsQcVmoldJWCpxTYmDr5OEuojBBUUF9sJuq7v89sHD9cAi8vwj+cM/rGZymWrSiZJpnPHBjNBUE05ZiKImxCxF6pjNOA7TYP/UuWfunXHOcbp/7OO7n3PPuXfvnNDMCpezpj6tSvX5A141HuvvIC1rgigCM2QlRpKkWqfd74CZGLVaJO1QZtEXh+qscvghGqP0f7UjosyjVT/Tnmqvxx6o8EMMRjFnVvb+vuqBEkt/9vm9Hpfqg1mlEPvYqQsYiIc4ugATgXiZzVXtcbr9PphdCgnyY4fZNBAPc+iouQTmyUoUHVUH83H2eN/q4bFIhIV6eAJnHzFJ6WPtA4Fyh6YXEEiUHdSNfn0mr+/0pIOK5sb1D+fmRnTxJIGnmPhlKmMyNWgRxUICTzNxfbqlcyCuXRNB/w99W4uQLp4h8CwTI398d/bWQ7smAqf+On7baojnCCQxcXVTVU7GdI8onifwAhPDdRM3ui/8owl7XvlwxlRIFy8SSGZiyHQ1ZUHWLU3kt2zJ/N4j6cJM4CUmfsytaZd/rhbFIgIvM3Fx9rljF36SRLGYQAoT33bcSyzMGqSiP9PaM7pjrSGWEFjKRH9Rt+KutYorlQksY+L8Zz2/Lf8yThTLCaQy0ftnTeK9k72ieIXACiY+PXp0xUcZXdo6nDffM8VGG+tII5Cuif6kYu/mmLAkCguBDCaOX0s2SRazKF4l8BoTpwa920a/sInidQIrmThfrN2yiCgyCaxiYiAraXTn0juisBJYzcQ3N5b0BD/M1YT3q5Tku2HjOX2DwBomBlMv5cQ96BTFWgJZTFyqzOwYr/xEFG8SyGbi8iJ5uuF0lSgQgRwmrpzIXRy8PC2KdQTW/7/YQGAjEyMf/01ub+gWxSYCmInrJQ63aeKaKN4isJmJmwV3p1LnXBFFLoG3mRizNo/Ik5Io8ghsYeLXk327Znw+IIqtBLYxEUmwt11c6NJEw5qJwrPj9BlTlQRtv6rwqqpb335spZAvY9SO2CaIkb+LfWiF7Y/GkB4LaDTzcQdGbdNG9LB9sxXeofEEHwtptBrRpr1HtUIR3YKP8VHBqOWOES36RMU0Woxo1mMJRofDfNxJo2RESY+7MGqu06Pvvj5RKY0yH3djdGiQj3toDPFxL41WPpZh1HSfj+U0GjfEF9GXVEGjg492GmU+qhiFBvkrqqTRxscqjBqH+OjAqEGIThrNfHwXIxLmo4vG+exC6JL69X9zH0YHG9nnR+J+jIIRY/FGdNOYzksPRge6eFmNUf0QH4FGCx+9GNVV89GHUW2Yj36MaoQYwCggzF5jPIFa7NWvvRYj7xAf6zACiY/1GLnDxl0y4gGMXGZeBjFy7OXjQYwqhXMSjOxCbMCoLMLHRox2h/gYwqhEiE0YFQnnPIRRwYARu/SHthmj7YiPhzHKF2ILRjZheCuNIT62qYHyMsVEv/g9+1RvmbtChXacfe597fhAiaY/uMv2q9ChaAOgM1Ce9h/iZUWs')







