import operator
import pickle
import re
import demoji
import pandas as pd
import numpy as np


def expand_vocab_coverage(df):
    with open('contraction_dict.pkl', 'rb') as file:
        contractions_dict = pickle.load(file)


    def contraction_expander(text):

        text = re.sub(chr(8217), "'", text)
        text = re.sub(chr(8216), "'", text)
        contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))

        def replace(match):
            return contractions_dict[match.group(0)]

        return contractions_re.sub(replace, text)


    def remove_urls(text):
        return re.sub(r"https?:\/\/t.co\/[A-Za-z0-9]+", "", text)


    def char_entity_references(text):
        text = re.sub(r"&gt;", ">", text)
        text = re.sub(r"&lt;", "<", text)
        return re.sub(r"&amp;", "&", text)


    def separate_punctuations(text):
        text = re.sub(chr(8230), "...", text)
        text = re.sub(chr(8220), '"', text)
        text = re.sub(chr(8221), '"', text)
        text = re.sub(chr(8216), "'", text)
        text = re.sub('~', 'around ', text)
        punctuations = '@#!?+&*[]-%.:/();$=><|{}^,"—' + "'`"
        for p in punctuations:
            text = text.replace(p, f' {p} ')

        text = text.replace(" .  .  .", ' ...')
        if " . . . " not in text:
            text = text.replace(" .  .", ' ...')
        return text


    def replace_emojis(text):
        skin_tones = ["Light Skin Tone", "Medium-Light Skin Tone", "Medium Skin Tone", "Medium-Dark Skin Tone",
                      'Dark Skin Tone']
        skin_tones = [sk.lower() for sk in skin_tones]
        text = demoji.replace_with_desc(text, sep=" ")
        for sk in skin_tones:
            text = re.sub(sk, "", text)
        return text


    def clean_hashtags_mentions(text):
        text = re.sub(r"VoteHimOut2020", "Vote Him Out 2020", text)
        text = re.sub(r"WhosTheBoss", "Who is the boss", text)
        text = re.sub(r"WhoDoesTrumpOwe", "Who does Trump owe", text)
        text = re.sub(r"CarnivoreBC2020", "Carnivore of British Columbia 2020", text)
        text = re.sub(r"menchies", "mentions", text)
        text = re.sub(r"PARABELLUM", "semiautomatic pistol", text)
        text = re.sub(r"TheIceFamily", "The Ice Family", text)
        text = re.sub(r"VoteEarly", "Vote Early", text)
        text = re.sub(r"wegotlove", "we got love", text)
        text = re.sub(r"OBiden", "Obama Biden", text)
        text = re.sub(r"ThenTheyPointTheFingerAtYou", "Then They Point The Finger At You", text)
        text = re.sub(r"BattleRap", "Battle Rap", text)
        text = re.sub(r"NationalVoterRegistrationDay", "National Voter Registration Day", text)
        text = re.sub(r"Bitchass", "bitch ass", text)
        text = re.sub(r"BeatDown", "beat down", text)
        text = re.sub(r"TeamBiden", "Team Biden", text)
        text = re.sub(r"WithBidenWeCan", "With Biden We Can", text)
        text = re.sub(r"ClassicMaterial", "Classic Material", text)
        text = re.sub(r"DefundThePolice", "Defund The Police", text)
        text = re.sub(r"STRENGTHENETH", "STRENGTHEN", text)
        text = re.sub(r"COVID__19", "Corona Virus 2019", text)
        text = re.sub(r"SHOxBET", "Show Time and Black Entertainment", text)
        text = re.sub(r'Uuum', "Um", text)
        text = re.sub(r"OwntheVote2020", "Own The Vote 2020", text)
        text = re.sub(r"CrackHouse", "Crack House", text)
        text = re.sub(r"ConspiracyQuacks", "Conspiracy Quacks", text)
        text = re.sub(r"RNCFactCheck", "Republican National Convention Fack Check", text)
        text = re.sub(r"DemocraticConvention", "Democratic Convention", text)
        text = re.sub(r"BODYCOUNT", "BODY COUNT", text)
        text = re.sub(r"ImVotingForJoe", "I Am Voting For Joe", text)
        text = re.sub(r"smōl", "extremely small", text)
        text = re.sub(r"FinalLevelTwitterGang", "Final Level Twitter Gang", text)
        text = re.sub(r"CORONAVIRUS", "CORONA VIRUS", text)
        text = re.sub(r"Enforceme", "Enforce me", text)
        text = re.sub(r"Trumpchaos", "Trump chaos", text)
        text = re.sub(r"puertorriqueños", "Puerto Ricans", text)
        text = re.sub(r"TutuolaTuesday", "Tutuola Tuesday", text)
        text = re.sub(r"SaveSocialSecurity", "Save Social Security", text)
        text = re.sub(r"BidenWonTheDebate", "Biden Won The Debate", text)
        text = re.sub(r"BidenHarrisToSaveAmerica", "Biden Harris To Save America", text)
        text = re.sub(r"BidenTownHall", "Biden Townhall", text)
        text = re.sub(r"HITBOY", "HIT BOY", text)
        text = re.sub(r"EasterEggs", "Easter Eggs", text)
        text = re.sub(r"سه", "three", text)
        text = re.sub(r"اعدام", "Execution", text)
        text = re.sub(r"Latinx", "Hispanic", text)
        text = re.sub(r"incel", "involuntarily celibate", text)
        text = re.sub(r"RNCConvention", "Republican National Convention", text)
        text = re.sub(r"все", "all", text)
        text = re.sub(r"FinalLevel", "Final Level", text)
        text = re.sub(r"TooBigToRig", "Too Big To Rig", text)
        text = re.sub(r"VPDebate", "Vice President Debate", text)
        text = re.sub(r"MakeAmericaGreatAgain", "Make America Great Again", text)
        text = re.sub(r'ICEMFT', "Ice Motherfucking Tea", text)
        text = re.sub(r"CarStuff", "Car Stuff", text)
        text = re.sub(r"AdvancedGame", "Advanced Game", text)
        text = re.sub(r"BlackLivesMatter", "Black Lives Matter", text)
        text = re.sub(r"BidenCalm", "Biden Calm", text)
        text = re.sub(r"BidenHarris2020", "Biden Harris 2020", text)
        text = re.sub(r"TrumpLiesAmericansDie", "Trump Lies Americans Die", text)
        text = re.sub(r"InIceColdBlood", "In Ice Cold Blood", text)
        text = re.sub(r"در", "at", text)
        text = re.sub(r"SVU22", "Special Victims Unit Season 22", text)
        text = re.sub(r"TrumpPenceFailure", "Trump Pence Failure", text)
        text = re.sub(r"ThrowBackThursday", "Throwback Thursday", text)
        text = re.sub(r"Bitchboy", "Bitch boy", text)
        text = re.sub(r"BuildBackBetter", "Build Back Better", text)
        text = re.sub(r"ObamaBiden", "Obama Biden", text)
        text = re.sub(r"Tfw", "Those feel when", text)
        text = re.sub(r"COVID19", "Corona Virus 2019", text)
        text = re.sub(r"TeamJoe", "Team Joe", text)
        text = re.sub(r"Cybertruck", "Cyber truck", text)
        text = re.sub(r"2020VISION", "2020 VISION", text)
        text = re.sub(r"WESTDAYEVER", "WEST DAY EVER", text)
        text = re.sub(r"UNFUCKWITHABLE", "CANNOT FUCK WITH ME", text)
        text = re.sub(r"QuarantineLife", "Quarantine Life", text)
        text = re.sub(r"covid|Covid19|Covid|COVID", "Corona Virus", text)
        text = re.sub(r"Debates2020", "Debates 2020", text)
        text = re.sub(r"DemConvention", "Democratic Convention", text)
        text = re.sub(r"TrumpKnewVoteBlue", "Trump Knew Vote Blue", text)
        text = re.sub(r"Clownass", "Clown Ass", text)
        text = re.sub(r"TrumpChaos", "Trump Chaos", text)
        text = re.sub(r"BodyCount", "Body Count", text)
        text = re.sub(r"moovin", "moving", text)
        text = re.sub(r"WeHaveHerBack", "We Have Her Back", text)
        text = re.sub(r"DontLookAway", "Do Not Look Away", text)
        text = re.sub(r"cucked", "cuckolded", text)
        text = re.sub(r"BidenWon", "Biden Won", text)
        text = re.sub(r"ChinaVirus", "China Virus", text)
        text = re.sub(r"sickomode", "sicko mode", text)
        text = re.sub(r"UNfollow", "Do not follow", text)
        text = re.sub(r"BidenHarris2020ToSaveAmerica", "Biden Harris 2020 To Save America", text)
        text = re.sub(r"Substack", "blog", text)
        text = re.sub(r"9Thousand", "Nine Thousand", text)
        text = re.sub(r"MomsForBiden", "Moms For Biden", text)
        text = re.sub(r"Uuuuuum", "Um", text)
        text = re.sub(r"surgic", "surgical", text)
        text = re.sub(r"QuarantineLife", "Quarantine Life", text)
        text = re.sub(r"SheGotItRight", "She Got It Right", text)
        text = re.sub(r"EditButton", "Edit Button", text)
        text = re.sub(r"TheOriginalConstitution", "The Original Constitution", text)
        text = re.sub(r"BlueWave2020", "Blue Wave 2020", text)
        text = re.sub(r"Hasidics", "Hasidic", text)
        text = re.sub(r"道場|dōjō", "Dojo", text)
        text = re.sub(r"doppelbanger", "doppelganger", text)
        text = re.sub(r"droneship", "drone ship", text)
        text = re.sub(r"TrumpInsecurity", "Trump Insecurity", text)
        text = re.sub(r"EscapeTraining", "Escape Training", text)
        text = re.sub(r"AdvancedGame2020", "Advanced Game 2020", text)
        text = re.sub(r"RNC2020", "Republican National Convention 2020", text)
        text = re.sub(r"Democrac", "Democrat", text)
        text = re.sub(r"LameStream", "Mainstream", text)
        text = re.sub(r"smea", "", text)
        text = re.sub(r"famleeeeee", "family", text)
        text = re.sub(r"SHLTR", "SHELTER", text)
        text = re.sub(r"CLTHNG", "CLOTHING", text)
        text = re.sub(r"UNFUCKWITH", "CANNOT FUCK WITH", text)
        text = re.sub(r"Wikigenius", "Wikipedia genius", text)
        text = re.sub(r"AMENDMEN", "AMENDMENT", text)
        text = re.sub(r"trumppencefailure", "Trump Pence Failure", text)
        text = re.sub(r"YouAreNext2022", "You Are Next 2022", text)
        text = re.sub(r"BotAlert", "Bot Alert", text)
        text = re.sub(r"OurCourt", "Our Court", text)
        text = re.sub(r"Truckers4Trump", "Truckers For Trump", text)
        text = re.sub(r"vote￼", "vote", text)
        text = re.sub(r"Unironically", "Not ironically", text)
        text = re.sub(r"Vibbbe", "Vibe", text)
        text = re.sub(r"Immigratio", "Immigration", text)
        text = re.sub(r"DumbFucks", "Dumb Fucks", text)
        text = re.sub(r"grandp", "grandpa", text)
        text = re.sub(r"DNC2020", "Democratic National Convention 2020", text)
        text = re.sub(r"KeepItG", "Keep It Gangster", text)
        text = re.sub(r"TOMORR", "TOMORROW", text)
        text = re.sub(r"QueensBridge", "Queens Bridge", text)
        text = re.sub(r"10gs", "ten thousand dollars", text)
        text = re.sub(r"FiveFingerDeathPunch", "Five Finger Death Punch", text)
        text = re.sub(r"2gthr", "together", text)
        text = re.sub(r"AHole", "Asshole", text)
        text = re.sub(r"LoveTip", "Love Tip", text)
        text = re.sub(r"welI", "well", text)
        text = re.sub(r"MakeTheLootLoop", "Make The Loot Loop", text)
        text = re.sub(r"preconditio", "precondition", text)
        text = re.sub(r"Hazl", "Hazel", text)
        text = re.sub(r"theaster", "easter", text)
        text = re.sub(r"permemently", "permanently", text)
        text = re.sub(r"disssing", "dissing", text)
        text = re.sub(r"Kantbot", "Kant Bot", text)
        text = re.sub(r"LeGend", "legend", text)
        text = re.sub(r"GetoBoys", "Get To Boys", text)
        text = re.sub(r"ChrisRock", "Chris Rock", text)
        text = re.sub(r"TRUMPCHAOS", "TRUMP CHAOS", text)
        text = re.sub(r"Hopefu", "Hopefully", text)
        text = re.sub(r"Covid_19", "Corona Virus 2019", text)
        text = re.sub(r"GeorgeFloyd", "George Floyd", text)
        text = re.sub(r"Мама", "Mama", text)
        text = re.sub(r"всем", 'all', text)
        text = re.sub(r"но", "but", text)
        text = re.sub(r"объяснить", 'explain', text)
        text = re.sub(r"Можно", 'can', text)
        text = re.sub(r'HoodPolitics', "Hood Politics", text)
        text = re.sub(r'SVU20', 'Special Victims Unit', text)
        text = re.sub(r"entour", "surroundings", text)
        text = re.sub(r"OUARANTINE", "QUARANTINE", text)
        text = re.sub(r"incompe", "incompetent", text)
        text = re.sub(r"Tmills", "Travis Mills", text)
        text = re.sub(r"RoshHashanah", "Rosh Hashanah", text)
        text = re.sub(r"822k", "822000", text)
        text = re.sub(r"WomensEqualityDay", "Womens Equality Day", text)
        text = re.sub(r"suppressi", "suppression", text)
        text = re.sub(r"TrumpsGestapo", "Trump Gestapo", text)
        text = re.sub(r"incels", "involuntary celibates", text)
        text = re.sub(r"APROVED", "APPROVED", text)
        text = re.sub(r"ModernWarfare", "Modern Warfare", text)
        text = re.sub(r"comeba", "come back", text)
        text = re.sub(r"7for7", "seven for seven", text)
        text = re.sub(r"ethnonarcissism", "ethnic narcissism", text)
        text = re.sub(r"wokeness", "being woke", text)
        text = re.sub(r"DoggPoun", "Dog Pound", text)
        text = re.sub(r"DonaldTrumpStandsFor", "Donald Trump Stands For", text)
        text = re.sub(r"BadAzz", "Badass", text)
        text = re.sub(r"RestInPeace", "Rest In Peace", text)
        text = re.sub(r"BC2020", "British Columbia", text)
        text = re.sub(r"infrastructu", "infrastructure", text)
        text = re.sub(r"FaceApp", "Face App", text)
        text = re.sub(r"100DaysToGo", "100 Days To Go", text)
        text = re.sub(r"این", "this", text)
        text = re.sub(r"است", "is", text)
        text = re.sub(r"انتظار", "Expectation", text)
        text = re.sub(r"قابل", "possible", text)
        text = re.sub(r"لحظه", "the moment", text)
        text = re.sub(r"هر", "any", text)
        text = re.sub(r"آنها", "they", text)
        text = re.sub(r"مرگ", "death", text)
        text = re.sub(r"به", "to the", text)
        text = re.sub(r"محکوم", "convicted", text)
        text = re.sub(r"تظاهرات", "demonstrations", text)
        text = re.sub(r"شرکت", "Company", text)
        text = re.sub(r"برای", "to", text)
        text = re.sub(r"Uhhhhhhhhhh", "Uh", text)
        text = re.sub(r"MachineHead", "Machine Head", text)
        text = re.sub(r"TrumpsChaos", "Trump Chaos", text)
        text = re.sub(r"PutinsGOPConvention", "Putin Grand Old Party Convention", text)
        text = re.sub(r"TheInfamous", "The Infamous", text)
        text = re.sub(r"Cybertr", "Cyber Truck", text)
        text = re.sub(r"Factorio", "Factory", text)
        text = re.sub(r"Speedrunning", "Speed running", text)
        text = re.sub(r"Maaaaaaan", "Man", text)
        text = re.sub(r"Croati", "Croatian", text)
        text = re.sub(r"SouthCentralLA", "South Central Los Angeles", text)
        text = re.sub(r"MFnStank", "Motherfucking Stank", text)
        text = re.sub(r"socialdilemma", "social dilemma", text)
        text = re.sub(r"Lesssgoooooooooooo", "Let us go", text)
        text = re.sub(r"IMVotingFor", "I Am Voting For", text)
        text = re.sub(r"Instea", "Instead", text)
        text = re.sub(r"VoteForScience", "Vote For Science", text)
        text = re.sub(r"PromAtThePolls", "Prom At The Polls", text)
        text = re.sub(r"EXACTL", "EXACTLY", text)
        text = re.sub(r"FaceTuned", "Face Tuned", text)
        text = re.sub(r"positionist", "position", text)
        text = re.sub(r"MakeAPlan", "Make A Plan", text)
        text = re.sub(r"TrumpFailure", "Trump Failure", text)
        text = re.sub(r"TrumpViolence", "Trump Violence", text)
        text = re.sub(r"wammin", "women", text)
        text = re.sub(r"TrumpLied200kDied", "Trump Lied 200000 Died", text)
        text = re.sub(r"FathersDay2019", "Fathers Day 2019", text)
        text = re.sub(r"Investigati", "Investigation", text)
        text = re.sub(r"UniteBehindTheScience", "Unite Behind The Science", text)
        text = re.sub(r"Disappo", "Disappointed", text)
        text = re.sub(r"CriticalBeatdown", "Critical Beatdown", text)
        text = re.sub(r"LetsMakeHerstory", "Lets Make Her Story", text)
        text = re.sub(r"WatchWhatYouSay", "Watch What You Say", text)
        text = re.sub(r"FredomOfSpeech", "Freedom Of Speech", text)
        text = re.sub(r"Ballin\\Flossin", "Balling Flossing", text)
        text = re.sub(r"HaterTube", "Hater tube", text)
        text = re.sub(r"demcovention", "Democratic Convention", text)
        text = re.sub(r'Judgemen', "Judge", text)
        text = re.sub(r"systemat", "system at", text)
        text = re.sub(r"SOILD", 'SOILED', text)
        text = re.sub(r"BLDNG", "BUILDING", text)
        text = re.sub(r"preexistin", "preexisting", text)
        text = re.sub(r"BidenHarris2020Landslide", "Biden Harris 2020 Landslide", text)
        text = re.sub(r"IAmADemocrat", "I Am A Democrat", text)
        text = re.sub(r"accountabily", "accountability", text)
        text = re.sub(r"TrumpBux", "Trump Box", text)
        text = re.sub(r"CopKiller", "Cop Killer", text)
        text = re.sub(r"heroes—", "heroes", text)
        text = re.sub(r"drpimplepopper", "Doctor Pimple Popper", text)
        text = re.sub(r"JWalking", "Jay Walking", text)
        text = re.sub(r"ThePeopleHaveHad", "The People Have Had", text)
        text = re.sub(r"HellYes", "Hell Yes", text)
        text = re.sub(r"FinalLevel", "Final Level", text)
        text = re.sub(r"Lallapalooza", 'concert', text)
        text = re.sub(r"Anarchis", "Anarchy", text)
        text = re.sub(r"BodyCounts", "Body Counts", text)
        text = re.sub(r"quixo", "quixotic", text)
        text = re.sub(r"HatersOccupation", "Haters Occupation", text)
        text = re.sub(r"LEZO", "let us go", text)
        text = re.sub(r"INDIVIDU", "INDIVIDUAL", text)
        text = re.sub(r"countenan", "countenance", text)
        text = re.sub(r"CLOWNASS", "CLOWN ASS", text)
        text = re.sub(r"SLAYIN", 'SLAYING', text)
        text = re.sub(r"GOPHypocrites", "Grand Old Party Hypocrites", text)
        text = re.sub(r"teamJOE", "Team Joe", text)
        text = re.sub(r"debates2020", "debates 2020", text)
        text = re.sub(r"whenev", "whenever", text)
        text = re.sub(r"ValentinesDay", "Valentines Day", text)
        text = re.sub(r"BROOOOOOOO", "BRO", text)
        text = re.sub(r"NeverForget", "Never Forget", text)
        text = re.sub(r"BlueWaveSenate", "Blue Wave Senate", text)
        text = re.sub(r"DumbfuckAlert", "Dumb fuck Alert", text)
        text = re.sub(r"HEROESAct", "HEROES Act", text)
        text = re.sub(r"JewishPrivilege", "Jewish Privilege", text)
        text = re.sub(r"happine", "happiness", text)
        text = re.sub(r"WomanMurdered", "Woman Murdered", text)
        text = re.sub(r"DEBATES2020", "DEBATES 2020", text)
        text = re.sub(r"uuuum", "um", text)
        text = re.sub(r"ironyposting", "irony posting", text)
        text = re.sub(r"RepealTheBan", "Repeal The Ban", text)
        text = re.sub(r"NoBanAct", "No Ban Act", text)
        text = re.sub(r"Division2", "Division", text)
        text = re.sub(r"repudia", "repudiate", text)
        text = re.sub(r"DEPENDANTS", 'DEPENDENTS', text)
        text = re.sub(r"StopSusan", "Stop Susan", text)
        text = re.sub(r"Honestl", "Honestly", text)
        text = re.sub(r"ArtOfRap", "Art Of Rap", text)
        text = re.sub(r"TrumpFailedChallenge", "Trump Failed Challenge", text)
        text = re.sub(r"IwasBrokeAF", "I was Broke As Fuck", text)
        text = re.sub(r"patriotnotpartisan", "patriot not partison", text)
        text = re.sub(r"CourageForThePeople", "Courage For The People", text)
        text = re.sub(r"demconvention", "Democratic Convention", text)
        text = re.sub(r"TENURED", "tenure", text)
        text = re.sub(r"2020Moovin", "moving", text)
        text = re.sub(r"TrumpsTaxReturns", "Trumps Tax Returns", text)
        text = re.sub(r"2CHNZ", "Two Chains", text)
        text = re.sub(r"COVIDー19", "Corona Virus", text)
        text = re.sub(r"memeing", "meme", text)
        text = re.sub(r"Netf", 'Netflix', text)
        text = re.sub(r"ˈfæʃɪzəm", "", text)
        text = re.sub(r"KamalaForVP", "Kamala For Vice President", text)
        text = re.sub(r"platinu", "platinum", text)
        text = re.sub(r"DonTheCon", "Don The Con", text)
        text = re.sub(r"UUUUUUM", "um", text)
        text = re.sub(r"RACISIM", "RACISM", text)
        text = re.sub(r"LatinosForTrump", "Latinos For Trump", text)
        text = re.sub(r"HowToAlly", "How To Ally", text)
        text = re.sub(r"spinaltap", "spinal tap", text)
        text = re.sub(r"slutshamed", "slut shamed", text)
        text = re.sub(r"DogBallin", "Dog Balling", text)
        text = re.sub(r"shitposter", "shit poster", text)
        text = re.sub(r"RepublicanConvention", "Republican Convention", text)
        text = re.sub(r"TwitterEdit", "Twitter Edit", text)
        text = re.sub(r"DemCast", "Democratic Cast", text)
        text = re.sub(r"OneTrickPhony", "One Trick Phony", text)
        text = re.sub(r"TrumpIsNotLikeYou", "Trump Is Not Like You", text)
        text = re.sub(r"unArmed", "unarmed", text)
        text = re.sub(r"promoing", "promotion", text)
        text = re.sub(r"SOMEBOD", "SOMEBODY", text)
        text = re.sub(r"SHLTRS", "SHELTERS", text)
        text = re.sub(r"constituen", "constituents", text)
        text = re.sub(r"150Thousand", "150000", text)
        text = re.sub(r"LaMelo", 'La Melo', text)
        text = re.sub(r"PortlandProtest", "Portland Protest", text)
        text = re.sub(r"CarStuff", "Car Stuff", text)
        text = re.sub(r"JusticeForBreonna", "Justice For Breonna", text)
        text = re.sub(r"LiarInChief", "Liar In Chief", text)
        text = re.sub(r"EqualStandardMovie", "Equal Standard Movie", text)
        text = re.sub(r"LethalWeaponMovie", "Lethal Weapon Movie", text)
        text = re.sub(r"Amendme", "Amendment", text)
        text = re.sub(r"BreonnaTalyor", "Breonna Taylor", text)
        text = re.sub(r"microcelebs", "micro celebrities", text)
        text = re.sub(r"campaignin", "campaigning", text)
        text = re.sub(r"AngelaDavis", "Angela Davis", text)
        text = re.sub(r"CourageforthePeople", "Courage For The People", text)
        text = re.sub(r"MasksOnGlovesOff", "Masks On Gloves Off", text)
        text = re.sub(r"Buuuuuuut", "but", text)
        text = re.sub(r"DonJr", "Don Jr", text)
        text = re.sub(r"realignmen", "realignment", text)
        text = re.sub(r"sinist", "sinister", text)
        text = re.sub(r"libcuck", "liberal cuckold", text)
        text = re.sub(r"HustlingBackwards", "Hustling Backwards", text)
        text = re.sub(r"rncFactCheck", "Republican National Convention Check", text)
        text = re.sub(r"RNChaos", "Republican National Convention Chaos", text)
        text = re.sub(r"Ordinar", "Ordinary", text)
        text = re.sub(r"YUGE", 'HUGE', text)
        text = re.sub(r"OwnTheVote2020", "Own The Vote 2020", text)
        text = re.sub(r"RIGGEDELECTION", "RIGGED ELECTION", text)
        text = re.sub(r"GhettoBoys", "Ghetto Boys", text)
        text = re.sub(r"TooShort", "Too Short", text)
        text = re.sub(r"shitpost", "shit post", text)
        text = re.sub(r"articu", "articulate", text)
        text = re.sub(r"NationalNewJerseyDay", "National New Jersey Day", text)
        text = re.sub(r"VirusQuarantineLife", "Virus Quarantine Life", text)
        text = re.sub(r"ICAFarmville", "farm", text)
        text = re.sub(r"tantr", "tantrum", text)
        text = re.sub(r"faildaughters", "fail daughters", text)
        text = re.sub(r"reconstruc", "reconstruction", text)
        text = re.sub(r"DearMichigan", "Dear Michigan", text)
        text = re.sub(r"BODYCOUNT", "BODY COUNT", text)
        text = re.sub(r"7thDeadlySin", "Seventh Deadly Sin", text)
        text = re.sub(r"covid19", "Corona Virus", text)
        text = re.sub(r"FreeRosa", "Free Rosa", text)
        text = re.sub(r"OnlyFans", "Only Fans", text)
        text = re.sub(r"selflessl", "selflessly", text)
        text = re.sub(r"HillaryKaine2016", "Hillary Kaine 2016", text)
        text = re.sub(r"TwoDollarHoller", "Two Dollar Holler", text)
        text = re.sub(r"DemConvention2020", "Democratic Convention 2020", text)
        text = re.sub(r"PatriotNotPartisan", "Patriot Not Partisan", text)
        text = re.sub(r"bewilderme", "bewilderment", text)
        text = re.sub(r"noooooow", "now", text)
        text = re.sub(r"DrugLords", "Drug Lords", text)
        text = re.sub(r"Lowrided", "Low rided", text)
        text = re.sub(r"Роган", "Rogan", text)
        text = re.sub(r"Джо", "Joe", text)
        text = re.sub(r"FinalLevelTwitterGang", "Final Level Twitter Gang", text)
        text = re.sub(r"oversocialized", "over socialized", text)
        text = re.sub(r"Russiagate", "Russia gate", text)
        text = re.sub(r"Laschposting", "Lasch posting", text)
        text = re.sub(r"IceTalks", "Ice Talks", text)
        text = re.sub(r"shadowbanned", "shadow banned", text)
        text = re.sub(r"Antifragility", "Anti fragility", text)
        text = re.sub(r"TRANSPARENTLY", "TRANSPARENT", text)
        text = re.sub(r"momsforbidden", "moms forbidden", text)
        text = re.sub(r"HateBreed", "Hate Breed", text)
        text = re.sub(r"NewJackHustler", "New Jack Hustler", text)
        text = re.sub(r"throne2", "throne", text)
        text = re.sub(r"CarnivoreBC2020", "Carnivore British Columbia", text)
        text = re.sub(r"FreeThemAllVA", "Free Them All", text)
        text = re.sub(r"DontDeportEver", "Do not Deport Ever", text)
        text = re.sub(r"SellOut", "Sell Out", text)
        text = re.sub(r"ImpeachBillBarr", "Impeach Bill Barr", text)
        text = re.sub(r"crabwalking", "crab walking", text)
        text = re.sub(r"IceMFT", "Ice Motherfucking Tea", text)
        text = re.sub(r"SVU21", "Special Victims Unit", text)
        text = re.sub(r"showtuners", "show tuners", text)
        text = re.sub(r"DickWolf", "Dick Wolf", text)
        text = re.sub(r"UnFinishedBussiness", "Unfinished Business", text)
        text = re.sub(r"понял", "got it", text)
        text = re.sub(r"Миша", "Misha", text)
        text = re.sub(r"INSPI", "INSPIRATION", text)
        text = re.sub(r'ConstitutionDay', "Constitution Day", text)
        text = re.sub(r"Demconvention", "Democratic Convention", text)
        text = re.sub(r"NMBR", "NUMBER", text)
        text = re.sub(r"MelaniaTapes", "Melania Tapes", text)
        text = re.sub(r"TrumpLiedAmericansDied", "Trump Lied Americans Died", text)
        text = re.sub(r"Wooowwwww", "Wow", text)
        text = re.sub(r"TheIceFamily", "The Ice Family", text)
        text = re.sub(r"33Yrs", "33 Years", text)
        text = re.sub(r"BreonnaTaylor", "Breonna Taylor", text)
        text = re.sub(r"NonHustlers", "No Hustlers", text)
        text = re.sub(r"HardWorker", "Hard Worker", text)
        text = re.sub(r"idpol", "identity politics", text)
        text = re.sub(r"HighSchools", "High Schools", text)
        text = re.sub(r"TrumpBounty", "Trump Bounty", text)
        text = re.sub(r"OpenLetterToRepublicans", "Open Letter To Republicans", text)
        text = re.sub(r"thankles", "thankless", text)
        text = re.sub(r"TheArtOfComedy", "The Art Of Comedy", text)
        text = re.sub(r"TrumpMustResign", "Trump Must Resign", text)
        text = re.sub(r"TruckJewelry", "Truck Jewelry", text)
        text = re.sub(r"allota", "a lot of", text)
        text = re.sub(r"GShit", "Gangster Shit", text)
        text = re.sub(r"WestSidin", "West Siding", text)
        text = re.sub(r"Waithing", "Waiting", text)
        text = re.sub(r"BeCounted", "Be Counted", text)
        text = re.sub(r"disag", "disagreement", text)
        text = re.sub(r"CoronaVirus", "Corona Virus", text)
        text = re.sub(r"ColdMcdonalds", "Cold McDonalds", text)
        text = re.sub(r"FINALL", "FINAL LEVEL", text)
        text = re.sub(r"BabyChanel", "Baby Chanel", text)
        text = re.sub(r"InHerHonor", "In Her Honor", text)
        text = re.sub(r"CaptainCovid", "Captain Covid", text)
        text = re.sub(r"NojusticeNoDerby", "No justice No Derby", text)
        text = re.sub(r"HairTrigger", "Hair Trigger", text)
        text = re.sub(r"Powernomics", "Power Economics", text)
        text = re.sub(r"BeatDown", "beat down", text)
        text = re.sub(r"RhymePays", "Rhyme Pays", text)
        text = re.sub(r"GoodAlwaysWins", "Good Always Wins", text)
        text = re.sub(r"DefendOurPostOffice", "Defend Our Post Office", text)
        text = re.sub(r"ImVoting4BidenBecause", "I am Voting For Biden Because", text)
        text = re.sub(r"VoteForHer", "Vote For Her", text)
        text = re.sub(r"NewYorkUndercover", "New York Undercover", text)
        text = re.sub(r"Turkposting", "Turk posting", text)
        text = re.sub(r"momentar", "momentarily", text)
        text = re.sub(r"paternit", "paternity", text)
        text = re.sub(r"longhauler", "long hauler", text)
        text = re.sub(r"chaaaaaarged", "charged", text)
        text = re.sub(r"libfem", "liberal feminists", text)
        text = re.sub(r"Hysterecto", "Hysterectomy", text)
        text = re.sub(r"MindFuck", "Mind Fuck", text)
        text = re.sub(r"Gucciman", "Gucci Man", text)
        text = re.sub(r"destigmitizing", "destigmatizing", text)
        text = re.sub(r"dsgnd", "designed", text)
        text = re.sub(r"chrstn", "christian", text)
        text = re.sub(r"undrcvr", 'undercover', text)
        text = re.sub(r"Bitchasses", "Bitch asses", text)
        text = re.sub(r"CountEveryVote", "Count Every Vote", text)
        text = re.sub(r"sorrynotsorry", "sorry not sorry", text)
        text = re.sub(r"BronxRiver", "Brox River", text)
        text = re.sub(r"RabbitHole", "rabbit hole", text)
        text = re.sub(r"moovin", "moving", text)
        text = re.sub(r"TrumpRacist", "Trump the Racist", text)
        text = re.sub(r"TrumpMeltdown", "Trump Meltdown", text)
        text = re.sub(r"trumpPencefailure", "Trump Pence failure", text)
        text = re.sub(r"autofiction", "auto fiction", text)
        text = re.sub(r"Hillaryite", "Hillary Supporter", text)
        text = re.sub(r"vaguesplain", "vaguely explain", text)
        text = re.sub(r"LoveIsLOUDER", "Love Is Louder", text)
        text = re.sub(r"TransRightsAreHumanRights", "Trans Rights Are Human Rights", text)
        text = re.sub(r"BidenIsBest", "Biden is the Best", text)
        text = re.sub(r"condescendin", "condescending", text)
        text = re.sub(r"girlboss", "girl boss", text)
        text = re.sub(r"TwitterNeedsEditButton", "Twitter Needs Edit Button", text)
        text = re.sub(r"malnourishe", "malnourished", text)
        text = re.sub(r"AwfulAbby", "awful Abby", text)
        text = re.sub(r"mybodymychoice", "my body my choice", text)
        text = re.sub(r"ConfederateMitch", "Confederate Mitch", text)
        text = re.sub(r"WeWantToPlay", "We Want To Play", text)
        text = re.sub(r"newnormal", "new normal", text)
        text = re.sub(r"AlyssaMilanoIsALie", "Alyssa Milano Is A Lie", text)
        text = re.sub(r"JusticeForBreonnaTaylor", "Justice For Breonna Taylor", text)
        text = re.sub(r"PollHero", "Poll Hero", text)
        text = re.sub(r"OwnTheVote", "Own The Vote", text)
        text = re.sub(r"LongHauler", "Long Hauler", text)
        text = re.sub(r"WearADamnMask", "Wear A Damn Mask", text)
        text = re.sub(r"DOPNESS", "DOPENESS", text)
        text = re.sub(r"liberatio", "liberation", text)
        text = re.sub(r"FlushTheTurdNov3rd", "Flush The Turn November 3rd", text)
        text = re.sub(r"KennethRossJr", "Kenneth Ross Jr", text)
        text = re.sub(r"TurnTexasBlue", "Turn Texas Blue", text)
        text = re.sub(r"ImVotingForBiden", "I am Voting For Biden", text)
        text = re.sub(r"Hilldawg", "Hillary dog", text)
        text = re.sub(r"TrumpHatesOurMilitary", "Trump Hates Our Military", text)
        text = re.sub(r"YangGang", "Yang Gang", text)
        text = re.sub(r"RepublicanNationalConvention", "Republican National Convention", text)
        text = re.sub(r"freeeeeeeeeee", "free", text)
        text = re.sub(r'TrumpKnew', "Trump Knew", text)
        return text

    df['cleaner_tweet'] = df['tweet'].apply(remove_urls)
    df['cleaner_tweet'] = df['cleaner_tweet'].apply(contraction_expander)

    df['cleaner_tweet'] = df['cleaner_tweet'].apply(char_entity_references)
    df['cleaner_tweet'] = df['cleaner_tweet'].apply(replace_emojis)
    df['cleaner_tweet'] = df['cleaner_tweet'].apply(separate_punctuations)
    df['cleaner_tweet'] = df['cleaner_tweet'].apply(clean_hashtags_mentions)

    glove_oov, glove_vocab_coverage, glove_text_coverage = get_text_vocab_coverage(df)

    print(f"glove vocab coverage: {glove_vocab_coverage}")
    print(f"glove text coverage: {glove_text_coverage}")

    return df


def get_text_vocab_coverage(df):
    glove_embeddings = np.load('models/glove.840B.300d.pkl', allow_pickle=True)

    def build_vocab(X):
        tweets = X.apply(lambda s: s.split()).values
        vocab = {}

        for tweet in tweets:
            for word in tweet:
                if vocab.get(word, ''):
                    vocab[word] += 1
                else:
                    vocab[word] = 1
        return vocab

    def check_embeddings_coverage(X, embeddings):
        vocab = build_vocab(X)
        covered = {}
        oov = {}
        n_covered = 0
        n_oov = 0

        for word in vocab:
            try:
                covered[word] = embeddings[word]
                n_covered += vocab[word]
            except:
                oov[word] = vocab[word]
                n_oov += vocab[word]

        vocab_coverage = len(covered) / len(vocab)

        text_coverage = (n_covered / (n_covered + n_oov))

        sorted_oov = sorted(oov.items(), key=operator.itemgetter(1))[::-1]

        return sorted_oov, vocab_coverage, text_coverage

    glove_oov, glove_vocab_coverage, glove_text_coverage = check_embeddings_coverage(df['cleaner_tweet'], glove_embeddings)

    return glove_oov, glove_vocab_coverage, glove_text_coverage


def resample_dataframe(df):
    ice_tea = df[df['user'] == "FINALLEVEL"]
    ice_t = ice_tea[ice_tea['word_count'] > 12]
    idx = ice_tea[~ice_tea.index.isin(ice_t.index)].index
    df = df[~df.index.isin(idx)]
    return df


def load_dataframe():
    with open("data/realDonaldTrump_tweets.pkl", 'rb') as file:
        dt = pickle.load(file)

    with open("data/Alyssa_Milano_tweets.pkl", 'rb') as file:
        am = pickle.load(file)

    with open("data/kanyewest_tweets.pkl", 'rb') as file:
        ye = pickle.load(file)

    with open("data/realDonaldTrump_tweets_2.pkl", 'rb') as file:
        dt2 = pickle.load(file)

    with open("data/kanyewest_tweets_2.pkl", 'rb') as file:
        ye2 = pickle.load(file)

    with open("data/FINALLEVEL_tweets_2.pkl", 'rb') as file:
        ice = pickle.load(file)

    with open("data/realDonaldTrump_tweets_v2.pkl", 'rb') as file:
        dt3 = pickle.load(file)

    with open("data/Alyssa_Milano_tweets_v2.pkl", "rb") as file:
        am3 = pickle.load(file)

    with open("data/kanyewest_tweets_v2.pkl", 'rb') as file:
        ye3 = pickle.load(file)

    with open("data/annakhachiyan_tweets_v2.pkl", "rb") as file:
        ak = pickle.load(file)

    with open("data/FINALLEVEL_tweets_v2.pkl", "rb") as file:
        ice2 = pickle.load(file)

    rdt = list(set(dt + dt2 + dt3))
    kye = list(set(ye + ye2 + ye3))
    ice = list(set(ice + ice2))
    ak = list(set(ak))
    am = list(set(am + am3))

    df = pd.DataFrame({"user":["realDonaldTrump"] * len(rdt) +
                               ["Alyssa_Milano"] * len(am) +
                               ["kanyewest"] * len(kye) +
                               ['FINALLEVEL'] * len(ice) +
                               ["annakhachiyan"] * len(ak),
                       "tweet": rdt + am + kye + ice + ak})

    df['word_count'] = df['tweet'].apply(lambda text: len(text.split()))
    return df


def main():
    df = load_dataframe()
    df = resample_dataframe(df)
    df = expand_vocab_coverage(df)
    df.to_csv("data/clean_tweets_rdt_kw_icet_am_ak.csv", index=False)




if __name__ == "__main__":
    main()