#What Is animagic

animagic is a tool (or set of tools) to allow easy downloading of
currently-running anime. It's intended for people who have a number of shows
they want to track, but aren't interested in manually downloading each new
episode.

#How does it work?

Basically it downloads the episodes for you from [nyaa.eu](http://nyaa.eu). It
finds them with some interesting scraping based on *format strings*,
specific to the anime and distributor you want. It downloads the torrent files
to the folder of your choice. Done!

#What must I do?

1. Create a file called config.yaml based on the example config in the repo.
   Required entries for each anime are: a web formatstring, and all the
   features used in that formatstring.
2. Set the script (*cli.py*) to be run regularly (daily, hourly, whatever).
   This script is what will actually update your local anime torrent files.
   Setting this up is probably easiest with cron under Linux -- see your
   distribution's documentation for more information on using cron.
3. Do something with the torrent files. This script does not download actual
   anime -- just the torrent files. You can watch the torrent directory with
   a tool like [transmission](http://www.transmissionbt.com/)'s daemon client.

#Format strings

The format strings use Python's own formatting language. See the [official
Python format string
specification](http://docs.python.org/library/string.html#format-string-syntax)
for detailed information on it. Note that the web format string must match
the torrent name on nyaa.eu **exactly**. This is to make sure that it is a
unique identifier.

Please note that the format string is passed over (i.e. formatted) twice: 
first the features are
inserted, and then in the second pass, any *episode* identifiers will be 
replaced with the episode number. The upshot of this is that you **must** give
the anime a feature that contains an '{episode}' string or variant thereof.
This feature should then be referenced in the format string in the location you
want the episode number to eventually be. 

One issue that comes up is when 
torrent providers use zero-filled episode numbers, for instance "01" instead of 
"1". The sample config shows a way to deal with this using the format string 
minilanguage and the two passes over the format string to zero-pad the episode 
number.
