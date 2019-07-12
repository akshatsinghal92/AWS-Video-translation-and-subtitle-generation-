from transcribeUtils import *
from srtUtils import *
import time
from videoUtils import *
from audioUtils import *



region='ap-south-1'
inbucket='videotest14335'
infile='Ralph-1080p.mp4'
outbucket='videotest14335output'
outfilename='subtitle'
outfiletype='mp4'

outlang=['es','hi','de']



# print out parameters and key header information for the user
print( "==> subtitle.py:\n")
print( "==> Parameters: ")
print("\tInput bucket/object: " + inbucket + infile )
print( "\tOutput bucket/object: " + outbucket + outfilename + "." + outfiletype )

print( "\n==> Target Language Translation Output: " )

for lang in outlang:
    print( "\t" + outbucket + outfilename + "-" + lang + "." + outfiletype)  
   
# Create Transcription Job
response = createTranscribeJob( region, inbucket, infile )

# loop until the job successfully completes
print( "\n==> Transcription Job: " + response["TranscriptionJob"]["TranscriptionJobName"] + "\n\tIn Progress"),

while( response["TranscriptionJob"]["TranscriptionJobStatus"] == "IN_PROGRESS"):
    print( "."),
    time.sleep( 30 )
    response = getTranscriptionJobStatus( response["TranscriptionJob"]["TranscriptionJobName"] )

print( "\nJob Complete")
print( "\tStart Time: " + str(response["TranscriptionJob"]["CreationTime"]) )
print( "\tEnd Time: "  + str(response["TranscriptionJob"]["CompletionTime"]) )
print( "\tTranscript URI: " + str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) )

# Now get the transcript JSON from AWS Transcribe
transcript = getTranscript( str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) ) 
# print( "\n==> Transcript: \n" + transcript)

# Create the SRT File for the original transcript and write it out.  
writeTranscriptToSRT( transcript, 'en', "subtitles-en.srt" )  
createVideo( infile, "subtitles-en.srt",outfilename + "-en." + outfiletype, "audio-en.mp3", True)

# Now write out the translation to the transcript for each of the target languages
for lang in outlang:
    writeTranslationToSRT(transcript, 'en', lang, "subtitles-" + lang + ".srt" , region)     
    
    #Now that we have the subtitle files, let's create the audio track
    createAudioTrackFromTranslation( region, transcript, 'en', lang, "audio-" + lang + ".mp3" )
    
    # Finally, create the composited video
    createVideo( infile, "subtitles-" + lang + ".srt", outfilename + "-" + lang + "." + outfiletype, "audio-" + lang + ".mp3", False)
