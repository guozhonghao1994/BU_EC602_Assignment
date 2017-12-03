""" EC602 Fall 2017

wordplayer checker for python and C++

(not quite complete)

Change `sourcecode` to the name of your program.
"""

sourcecode = None
#sourcecode = "wordplayer.py"
sourcecode = "wordplayer.cpp"

if not sourcecode:
    print('please edit this file and set the value of `sourcecode` to choose py or cpp to check')
    exit()


import unittest
import subprocess
import time
import os
import urllib.request
import random
import pep8

from subprocess import PIPE,Popen

Tests_Short=[
('macabre 6',[]),
('macabre 5',['cream']),
('macabre 4',[]),
('leap 4', ['leap', 'peal']),
('apoplectic 7',[]),
('apoplectic 6',[]),
('apoplectic 5',['apple']),
('apoplectic 4',['leap', 'peal']),
('abcdabcd 4',['aabb', 'abcd', 'adad', 'bbaa', 'daad', 'dada', 'dcab']),
('abcdabcd 3',['aab', 'aac', 'aad']),
('aabcbc 3',['aab', 'aac']),
]

Tests_Big=[
('anechocixq 8',['anechoic']),
('hemangiomatacountermarch 17',[]),
('testthisprogram 11',['prostatites', 'prosthetist', 'seismograph', 'straightest', 'thermistors', 'thermostats']),
]


Tests_Speed = [
({'cpp':0.000208,'py':0.000294},'on 2',['no','on'],),
({'cpp':6.57e-05,'py':0.000123},'act 3',['act', 'cat']),
({'cpp':0.00087,'py':0.01757},'apoplecticmacabre 5',['abaca', 'abaci', 'abamp', 'abate', 'abeam', 'abele', 'abler', 'aboil', 'aboma', 'abort', 'acari', 'acerb', 'aceta', 'acmic', 'actor', 'aecia', 'aerie', 'aimer', 'alamo', 'alarm', 'alate', 'alert', 'altar', 'alter', 'amber', 'ambit', 'amble', 'ameba', 'ameer', 'amice', 'amole', 'amort', 'ample', 'aorta', 'apace', 'apart', 'aport', 'appal', 'appel', 'apple', 'apter', 'areae', 'areal', 'areca', 'areic', 'arete', 'ariel', 'armet', 'aroma', 'artal', 'artel', 'atria', 'atrip', 'bacca', 'baler', 'baric', 'becap', 'belie', 'beret', 'berme', 'betel', 'biome', 'biota', 'birle', 'biter', 'blame', 'blare', 'blate', 'blear', 'bleat', 'bleep', 'blimp', 'blite', 'bloat', 'boart', 'bocce', 'bocci', 'boite', 'bolar', 'boral', 'boric', 'botel', 'brace', 'bract', 'brail', 'bream', 'broil', 'brome', 'cabal', 'caber', 'cable', 'cacao', 'cacti', 'caeca', 'camel', 'cameo', 'campi', 'campo', 'caper', 'carat', 'carbo', 'caret', 'carle', 'carob', 'carol', 'carom', 'carpi', 'carte', 'cater', 'cecal', 'ceiba', 'celeb', 'celom', 'ceorl', 'cerci', 'ceria', 'ceric', 'cibol', 'circa', 'citer', 'claim', 'clamp', 'clapt', 'claro', 'clear', 'cleat', 'clepe', 'clept', 'climb', 'clime', 'clipt', 'clomb', 'clomp', 'coact', 'coala', 'coapt', 'coati', 'cobia', 'coble', 'cobra', 'cocci', 'colic', 'comae', 'comal', 'combe', 'comer', 'comet', 'comic', 'compt', 'comte', 'copal', 'coper', 'copra', 'coral', 'coria', 'craal', 'cramp', 'crape', 'crate', 'cream', 'creel', 'creep', 'creme', 'crepe', 'crept', 'crime', 'crimp', 'cripe', 'croci', 'eater', 'eclat', 'elate', 'elect', 'elemi', 'elite', 'elope', 'embar', 'ember', 'emote', 'epact', 'erect', 'erica', 'etape', 'ileac', 'impel', 'irate', 'laari', 'labia', 'labor', 'labra', 'lacer', 'lamer', 'lamia', 'laree', 'later', 'leapt', 'leper', 'lepta', 'liber', 'libra', 'limba', 'limbo', 'limpa', 'lirot', 'liter', 'litre', 'lobar', 'loper', 'lotic', 'macer', 'macle', 'macro', 'maile', 'malar', 'malic', 'maple', 'maria', 'mater', 'mbira', 'mecca', 'melic', 'merit', 'merle', 'metal', 'meter', 'metre', 'metro', 'micra', 'micro', 'miler', 'milpa', 'miter', 'mitre', 'moira', 'moire', 'molar', 'moper', 'morae', 'moral', 'morel', 'motel', 'oater', 'obeli', 'ocrea', 'octal', 'oiler', 'oleic', 'omber', 'ombre', 'opera', 'optic', 'orate', 'orbit', 'oriel', 'pacer', 'palea', 'paler', 'palet', 'palpi', 'pampa', 'papal', 'paper', 'pareo', 'parle', 'parol', 'pater', 'patio', 'peace', 'pearl', 'peart', 'pepla', 'perea', 'peril', 'petal', 'peter', 'pibal', 'pical', 'picot', 'piece', 'pieta', 'pilar', 'pilea', 'pilot', 'pipal', 'piper', 'pipet', 'place', 'plait', 'plate', 'pleat', 'plebe', 'plica', 'plier', 'polar', 'poler', 'praam', 'prate', 'price', 'prima', 'prime', 'primo', 'primp', 'probe', 'proem', 'prole', 'rabat', 'rabic', 'ramee', 'ramet', 'ramie', 'ratal', 'ratel', 'ratio', 'react', 'realm', 'reata', 'rebec', 'rebel', 'rebop', 'recap', 'recce', 'recta', 'recti', 'recto', 'relet', 'relic', 'relit', 'remap', 'remet', 'remit', 'reoil', 'repel', 'repot', 'retem', 'retia', 'retie', 'riata', 'roble', 'taber', 'tabla', 'table', 'tabor', 'talar', 'taler', 'tamal', 'tamer', 'taper', 'tapir', 'taroc', 'telae', 'telia', 'telic', 'teloi', 'tempi', 'tempo', 'tepal', 'terai', 'terce', 'tiara', 'tical', 'tiler', 'timer', 'toile', 'topee', 'toper', 'topic', 'toric', 'trace', 'trail', 'tramp', 'triac', 'trial', 'tribe', 'trice', 'triol', 'tripe', 'tromp', 'trope']),
({'cpp':0.000325,'py':0.0049},'psychohistoriannoncollector 15',['anthropocentric', 'chancellorships', 'contrapositions', 'controllerships', 'cooperationists', 'corticotrophins', 'ethnohistorians', 'ethnohistorical', 'interscholastic', 'introspectional', 'ionospherically', 'neocolonialists', 'noncooperations', 'noncorrelations', 'nonpsychiatrist', 'prehistorically', 'protohistorians', 'psychohistorian', 'synchronisation', 'thyrocalcitonin']),
({'cpp':0.00118,'py':0.0391},'punishableanglerfishes 10',['airinesses', 'anablepses', 'anageneses', 'anagenesis', 'anglerfish', 'aphaereses', 'aphaeresis', 'aspergilla', 'aspergilli', 'assignable', 'aubergines', 'ballerinas', 'barenesses', 'baseliners', 'beleaguers', 'bengalines', 'bilinguals', 'billfishes', 'bleariness', 'bluefishes', 'bluenesses', 'bluishness', 'braininess', 'burnishing', 'bushelling', 'eelgrasses', 'enfeebling', 'enfleurage', 'engineries', 'enshrinees', 'ensphering', 'enuresises', 'epigenesis', 'euphrasies', 'fairnesses', 'fellnesses', 'fiberglass', 'fibreglass', 'filariases', 'finenesses', 'fingernail', 'flashiness', 'fleshiness', 'frangipane', 'frangipani', 'freebasing', 'freshening', 'fullerenes', 'fullnesses', 'furbishing', 'furnishing', 'galleasses', 'galliasses', 'garishness', 'garnishees', 'generalise', 'glibnesses', 'graininess', 'greaseball', 'greaseless', 'greasiness', 'greenflies', 'grisailles', 'grisliness', 'halenesses', 'halfnesses', 'hanselling', 'harnessing', 'harshening', 'highfliers', 'highnesses', 'hirselling', 'hugenesses', 'hungriness', 'inarguable', 'infeasible', 'inselberge', 'inselbergs', 'insensible', 'insphering', 'langlaufer', 'languisher', 'languishes', 'leannesses', 'liberalise', 'linearises', 'lungfishes', 'nasalising', 'nearnesses', 'nebulising', 'nephelines', 'neuralgias', 'nighnesses', 'nullifiers', 'painfuller', 'palenesses', 'palliasses', 'panellings', 'pangeneses', 'pangenesis', 'parfleshes', 'passengers', 'passerines', 'pearlashes', 'pellagrins', 'penalising', 'peninsular', 'peninsulas', 'perennials', 'perihelial', 'perishable', 'persiflage', 'phalangers', 'pilferable', 'pilferages', 'pingrasses', 'plagiaries', 'plagiarise', 'planishers', 'planishing', 'pleasuring', 'plenishing', 'pleurisies', 'plushiness', 'preassigns', 'prebilling', 'preblesses', 'prehensile', 'presageful', 'preselling', 'publishers', 'publishing', 'puninesses', 'punishable', 'purenesses', 'railbusses', 'realnesses', 'reeligible', 'refinishes', 'refuelling', 'reinfusing', 'relabeling', 'releasable', 'relishable', 'repaneling', 'repassages', 'repealable', 'resealable', 'reshingles', 'respelling', 'rifenesses', 'ringhalses', 'ripenesses', 'safranines', 'sailfishes', 'sailplaner', 'sailplanes', 'salesgirls', 'seafarings', 'serialises', 'serpigines', 'shanghaier', 'sharpening', 'shearlings', 'shellfires', 'shinneries', 'shrillness', 'signalises', 'signallers', 'sinfulness', 'singleness', 'singspiels', 'slanginess', 'sleepiness', 'spinneries', 'spiralling', 'suberising', 'subleasing', 'subpenaing', 'sullenness', 'superbness', 'supergenes', 'supersales', 'supersells', 'supineness', 'surpassing', 'uglinesses', 'uneasiness', 'unfairness', 'unfeasible', 'ungainlier', 'unleashing', 'unpassable', 'unpleasing', 'unreliable', 'unripeness', 'unshelling', 'unsphering', 'urbanising', 'usableness']),
({'cpp':0.00013,'py':0.000152},'anechocixq 8',['anechoic']),
({'cpp':0.00336,'py':0.05306},'psychohistoriannoncollector 8',
['accentor', 'acceptor', 'acentric', 'acetonic', 'acetylic', 'achiness', 'achiotes', 'acolytes', 'aconites', 'aconitic', 'acrolect', 'acrolein', 'acrolith', 'acrostic', 'acrylics', 'actinons', 'actorish', 'actressy', 'acyloins', 'aerolith', 'aerosols', 'ailerons', 'ainsells', 'airholes', 'airiness', 'airliner', 'airlines', 'airports', 'airposts', 'airships', 'airstrip', 'alcohols', 'alencons', 'alienist', 'alienors', 'allicins', 'allotter', 'allotype', 'allspice', 'alnicoes', 'alopecic', 'alphorns', 'alphosis', 'alpinely', 'alpinist', 'althorns', 'altoists', 'ancestor', 'ancestry', 'anchoret', 'ancients', 'anechoic', 'anethols', 'anilines', 'anisoles', 'annoyers', 'anointer', 'anolytes', 'anoretic', 'anorthic', 'anterior', 'anthesis', 'anthills', 'anticity', 'antihero', 'antiphon', 'antipill', 'antipole', 'antiporn', 'antipyic', 'antiriot', 'antiroll', 'antiship', 'antislip', 'antitype', 'antlions', 'antrorse', 'antsiest', 'aoristic', 'aphelion', 'aphonics', 'aphorise', 'aphorist', 'apocrine', 'apostils', 'apostles', 'apricots', 'apyretic', 'archines', 'archness', 'arcsines', 'arnottos', 'arsenics', 'arsonist', 'articles', 'artiness', 'artistes', 'artistic', 'artistry', 'artsiest', 'ascetics', 'asperity', 'aspersor', 'aspheric', 'aspirers', 'aspirins', 'assentor', 'assertor', 'assorter', 'asthenic', 'astonies', 'astonish', 'astricts', 'atechnic', 'atheists', 'athletic', 'atrocity', 'atrophic', 'atropine', 'atropins', 'attorney', 'cachepot', 'calcines', 'calcites', 'calcitic', 'caliches', 'calicles', 'calicoes', 'calipers', 'calliope', 'calliper', 'calloses', 'calorics', 'calories', 'calottes', 'calotype', 'caloyers', 'calthrop', 'caltrops', 'calycine', 'calycles', 'calypsos', 'calypter', 'canephor', 'caninity', 'canister', 'canities', 'cannelon', 'canniest', 'cannonry', 'canoeist', 'canoness', 'canonise', 'canonist', 'canopies', 'canticle', 'cantrips', 'capelins', 'capitols', 'caponier', 'capricci', 'caprices', 'capriole', 'capsicin', 'capstone', 'captions', 'carillon', 'carioles', 'carlines', 'caroches', 'carolers', 'caroller', 'carotins', 'carpools', 'carports', 'carrells', 'carriole', 'carrions', 'carritch', 'carrotin', 'carryons', 'cartoons', 'cartoony', 'caryotin', 'cashiers', 'catchers', 'catchier', 'catechin', 'catechol', 'cathects', 'catholic', 'cationic', 'cellists', 'celosias', 'cenotaph', 'centrals', 'centrist', 'ceorlish', 'cephalic', 'cephalin', 'ceratins', 'cesspool', 'chaconne', 'chalices', 'challies', 'challoth', 'chalones', 'chancels', 'chancery', 'chancier', 'chancily', 'chancres', 'channels', 'chansons', 'chanters', 'chanteys', 'chanties', 'chantors', 'chaperon', 'chapiter', 'chaplets', 'chapters', 'chariest', 'chariots', 'charleys', 'charlies', 'charnels', 'charpoys', 'charters', 'chartist', 'chastely', 'chastens', 'chastest', 'chastise', 'chastity', 'chattels', 'chatters', 'chattery', 'chattier', 'chattily', 'chayotes', 'cheapish', 'chelator', 'cheroots', 'chiastic', 'chicaner', 'chicanes', 'chicanos', 'chiccory', 'chicness', 'chiliast', 'chillers', 'chillest', 'chillier', 'chillies', 'chinches', 'chinless', 'chinones', 'chintses', 'chirpers', 'chirpier', 'chirpily', 'chitchat', 'chitlins', 'chitosan', 'chitters', 'chitties', 'chlorals', 'chlorate', 'chlorine', 'chlorins', 'chlorite', 'choicely', 'choicest', 'cholates', 'cholents', 'choleras', 'choleric', 'cholines', 'choosers', 'choosier', 'chopines', 'chorales', 'chorally', 'chorines', 'chorions', 'chortler', 'chortles', 'christen', 'christie', 'chronics', 'chronons', 'chthonic', 'ciceroni', 'cilantro', 'ciliates', 'cinchona', 'cineasts', 'cinerary', 'cinerins', 'cipolins', 'circlers', 'circlets', 'cisterna', 'cisterns', 'cistrons', 'citation', 'citators', 'citatory', 'citherns', 'cithrens', 'citrates', 'citrines', 'citterns', 'clannish', 'clarinet', 'clarions', 'clashers', 'claspers', 'classico', 'classier', 'classily', 'clastics', 'clatters', 'clattery', 'clayiest', 'clerical', 'cliental', 'clincher', 'clinches', 'clinical', 'clitoral', 'clitoric', 'clitoris', 'cloister', 'clothier', 'clysters', 'coachers', 'coaction', 'coactors', 'coalhole', 'coaliest', 'coalless', 'coalpits', 'coanchor', 'coarsely', 'coarsens', 'coarsest', 'coasters', 'coatless', 'cocaines', 'cochairs', 'cochlear', 'cochleas', 'cocinera', 'cocottes', 'coenacts', 'coercion', 'cohesion', 'cohoshes', 'cointers', 'coistrel', 'coistril', 'coitally', 'coitions', 'colessor', 'colicine', 'colicins', 'colinear', 'colistin', 'collapse', 'collaret', 'collates', 'collator', 'collects', 'colliers', 'colliery', 'collyria', 'colocate', 'colonels', 'colonial', 'colonics', 'colonies', 'colonise', 'colonist', 'colophon', 'colorant', 'colorers', 'colorist', 'colossal', 'colpitis', 'conation', 'conceals', 'conceits', 'concents', 'concepts', 'concerns', 'concerti', 'concerto', 'concerts', 'conchies', 'conciser', 'concocts', 'conepatl', 'conicity', 'coniines', 'conioses', 'coniosis', 'connects', 'connotes', 'consents', 'consoler', 'consoles', 'consorts', 'conspire', 'constant', 'contacts', 'contains', 'contents', 'contests', 'contorts', 'contract', 'contrail', 'contrary', 'contrast', 'contrite', 'controls', 'coolants', 'coolness', 'cooncans', 'coonties', 'cooption', 'coparent', 'copastor', 'copatron', 'copilots', 'coprince', 'copycats', 'copyists', 'coracles', 'corantos', 'cornetcy', 'cornices', 'corniche', 'cornicle', 'corniest', 'cornpone', 'corollas', 'coronach', 'coronals', 'coronary', 'coronate', 'coronels', 'coroners', 'coronets', 'corotate', 'corporal', 'corrects', 'corsairs', 'corsetry', 'corslets', 'cortical', 'cortices', 'cortisol', 'coscript', 'cosecant', 'costlier', 'costrels', 'cotenant', 'cotillon', 'cottiers', 'cranches', 'crannies', 'crashers', 'cratches', 'cratonic', 'creatins', 'creation', 'creators', 'creosols', 'cresylic', 'crinites', 'criollos', 'crispate', 'crispens', 'crispers', 'crispest', 'crispier', 'crispily', 'cristate', 'criteria', 'critical', 'critters', 'croceins', 'crochets', 'crocoite', 'crooners', 'cropless', 'crosiers', 'crosslet', 'crosstie', 'crotches', 'crotchet', 'cryolite', 'cryonics', 'cryostat', 'cryotron', 'crystals', 'cyanines', 'cyanites', 'cyanitic', 'cyanoses', 'cyanosis', 'cyanotic', 'cycasins', 'cyclases', 'cyclecar', 'cyclical', 'cyclists', 'cyclitol', 'cyclonal', 'cyclones', 'cyclonic', 'cycloses', 'cyclosis', 'cyprians', 'cysteins', 'cystines', 'cystitis', 'cytaster', 'cytosine', 'cytosols', 'earlship', 'earshots', 'earthily', 'eclipsis', 'ecliptic', 'eclosion', 'ecotonal', 'ecotypic', 'ecstatic', 'ectopias', 'ectosarc', 'elastics', 'elastins', 'elations', 'elicitor', 'elisions', 'elitists', 'ellipsis', 'elliptic', 'enactors', 'enactory', 'enations', 'enchains', 'enchants', 'enchoric', 'enclasps', 'enclitic', 'encroach', 'encrypts', 'encyclic', 'enscroll', 'ensnarls', 'entastic', 'enthalpy', 'enthrall', 'enthrals', 'entrails', 'entrains', 'entrants', 'entropic', 'eolithic', 'epically', 'epicotyl', 'epinasty', 'episcias', 'epistasy', 'epitasis', 'epsilons', 'erasions', 'eristics', 'erosions', 'erotical', 'errantly', 'erratics', 'erythron', 'escallop', 'escalops', 'escapist', 'eschalot', 'escolars', 'espartos', 'estriols', 'etchants', 'ethanols', 'ethicals', 'ethician', 'ethicist', 'ethinyls', 'ethnarch', 'ethnical', 'hairiest', 'hairless', 'hairline', 'hairnets', 'hairpins', 'halcyons', 'haltless', 'haplites', 'haplonts', 'haploses', 'haplosis', 'haptenic', 'harelips', 'haricots', 'harlotry', 'harpists', 'harpoons', 'harshens', 'harshest', 'harslets', 'hastiest', 'hatchels', 'hatchers', 'hatchery', 'hatchets', 'heartily', 'hectical', 'hecticly', 'heirship', 'heliasts', 'helicity', 'helicons', 'helicopt', 'heliport', 'helistop', 'hellcats', 'hellions', 'hencoops', 'heparins', 'hepatics', 'heptarch', 'heritors', 'heroical', 'herstory', 'hesitant', 'hierarch', 'hieratic', 'hilarity', 'hilliest', 'hilltops', 'hiltless', 'hiplines', 'hipsters', 'histones', 'historic', 'hitchers', 'hitherto', 'hoariest', 'hoarsely', 'hoarsens', 'hoarsest', 'hoisters', 'holiness', 'holistic', 'holotype', 'holstein', 'holsters', 'honestly', 'honorary', 'honorers', 'hoopless', 'hoopster', 'hootches', 'hootiest', 'hoplites', 'hoplitic', 'horniest', 'hornists', 'hornitos', 'hornless', 'horntail', 'horsecar', 'horsiest', 'hospices', 'hospital', 'hospitia', 'hostelry', 'hostiles', 'hostlers', 'hotchpot', 'hotlines', 'hotpress', 'hotshots', 'hyacinth', 'hyalines', 'hyalites', 'hyoscine', 'hyperons', 'hypnoses', 'hypnosis', 'hypnotic', 'hyponeas', 'hyponoia', 'hypothec', 'hysteria', 'hysteric', 'ichnites', 'ichthyic', 'iconical', 'icterics', 'illation', 'inaction', 'inarches', 'inceptor', 'inchoate', 'incisors', 'incisory', 'incitant', 'inciters', 'inclasps', 'incliner', 'inclines', 'incloser', 'incloses', 'incorpse', 'inearths', 'inerrant', 'inertial', 'inertias', 'inhalers', 'inherits', 'inhesion', 'inlayers', 'innately', 'innocent', 'inosites', 'inositol', 'insanely', 'insanest', 'insanity', 'inscapes', 'inscroll', 'insectan', 'insheath', 'inshrine', 'insister', 'insnarer', 'insnares', 'insolate', 'insolent', 'inspects', 'inspirer', 'inspires', 'installs', 'instance', 'instancy', 'instants', 'instates', 'instills', 'instinct', 'intently', 'interact', 'interior', 'interlap', 'interlay', 'internal', 'inthrall', 'inthrals', 'inthrone', 'intitles', 'intonate', 'intoners', 'intrants', 'intreats', 'intrench', 'introits', 'introrse', 'irenical', 'ironical', 'ironists', 'ironness', 'irritant', 'irritate', 'isatines', 'isochore', 'isochors', 'isochron', 'isocline', 'isocracy', 'isohyets', 'isolates', 'isolator', 'isolines', 'isopachs', 'isophote', 'isopleth', 'isospory', 'isotachs', 'isotones', 'isotonic', 'isotopes', 'isotopic', 'isotropy', 'isotypes', 'isotypic', 'itchiest', 'laciness', 'lacrosse', 'lactones', 'lactonic', 'lactoses', 'laicises', 'lanciers', 'lanoline', 'lanolins', 'lanosity', 'lanterns', 'lanthorn', 'latchets', 'latently', 'lathiest', 'latinity', 'latosols', 'latrines', 'latterly', 'lattices', 'lecithin', 'lections', 'lecythis', 'lenition', 'leprotic', 'leptonic', 'liaisons', 'licensor', 'lichenin', 'licorice', 'linchpin', 'linearly', 'lintiest', 'lintless', 'lioniser', 'lionises', 'lipocyte', 'litanies', 'literacy', 'literals', 'literary', 'literati', 'lithosol', 'littlish', 'littoral', 'loathers', 'localise', 'localist', 'localite', 'locality', 'locaters', 'location', 'locators', 'loessial', 'looniest', 'loophole', 'loopiest', 'loricate', 'loriners', 'lornness', 'lothario', 'loyalest', 'loyalist', 'lynchers', 'lynchpin', 'lyophile', 'lyricise', 'lyricist', 'nailsets', 'naphthol', 'naphthyl', 'naphtols', 'napoleon', 'narceins', 'narcissi', 'narcists', 'narcoses', 'narcosis', 'narcotic', 'nascency', 'nastiest', 'nathless', 'necropsy', 'necrosis', 'necrotic', 'neoliths', 'nephrons', 'nepotist', 'nicotine', 'nicotins', 'nictates', 'niellist', 'ninepins', 'ninnyish', 'nitchies', 'nitinols', 'nitrates', 'nitrator', 'nitriles', 'nitrites', 'nitrolic', 'nitrosyl', 'noisiest', 'nonactor', 'nonclass', 'noncolor', 'nonentry', 'nonionic', 'nonlocal', 'nonparty', 'nonpasts', 'nonplays', 'nonpoint', 'nonpolar', 'nonprint', 'nonroyal', 'nonsolar', 'nonstory', 'nonstyle', 'nontitle', 'nontonal', 'northern', 'northers', 'nostrils', 'notaries', 'notation', 'notchers', 'noticers', 'notional', 'notornis', 'nystatin', 'occasion', 'occipita', 'ocotillo', 'octanols', 'octarchy', 'octonary', 'octoroon', 'oestrins', 'oestriol', 'oilcloth', 'oilholes', 'oiliness', 'oilstone', 'olorosos', 'onanists', 'oophytes', 'oophytic', 'oospores', 'oosporic', 'oothecal', 'opalines', 'opencast', 'operants', 'operatic', 'operator', 'opinions', 'opsonins', 'optician', 'opticist', 'optional', 'oralists', 'orations', 'oratorio', 'oratress', 'orchises', 'orchitic', 'orchitis', 'orcinols', 'oriental', 'ornately', 'ornithes', 'ornithic', 'orphical', 'orphreys', 'orthicon', 'orthoepy', 'orthoses', 'orthosis', 'orthotic', 'ortolans', 'oscinine', 'oscitant', 'osteitic', 'osteitis', 'ostinato', 'ostiolar', 'ostioles', 'ostracon', 'otiosely', 'otiosity', 'otocysts', 'otoliths', 'otoscope', 'otoscopy', 'pachisis', 'pactions', 'painches', 'painless', 'painters', 'paintier', 'paisleys', 'paleosol', 'paletots', 'palliest', 'paltrier', 'paltrily', 'panelist', 'panicles', 'panniers', 'panoches', 'pantheon', 'panthers', 'pantiles', 'pantries', 'parchesi', 'parchisi', 'paretics', 'parhelic', 'parishes', 'parities', 'parritch', 'parsleys', 'parsonic', 'particle', 'partiers', 'partlets', 'partners', 'partyers', 'pasterns', 'pasticci', 'pastiche', 'pastiest', 'pastille', 'pastries', 'patchers', 'patchier', 'patchily', 'patently', 'patentor', 'pathetic', 'pathless', 'pathoses', 'patients', 'patriots', 'patronly', 'patroons', 'patterns', 'payrolls', 'peccancy', 'pecorini', 'pecorino', 'pectoral', 'pelicans', 'pelorian', 'pelorias', 'peltasts', 'penality', 'penchant', 'penicils', 'pennants', 'pensions', 'pentanol', 'pentarch', 'pentosan', 'perianth', 'perillas', 'periotic', 'perisarc', 'perlitic', 'persalts', 'personal', 'personas', 'pertains', 'petiolar', 'petition', 'petrolic', 'petrosal', 'peytrals', 'phaetons', 'phallist', 'pharoses', 'phelonia', 'phenolic', 'phenylic', 'philters', 'philtres', 'phonates', 'phonetic', 'phoniest', 'phorates', 'photonic', 'photoset', 'phratric', 'phreatic', 'phthalic', 'phthalin', 'phthises', 'phthisic', 'phthisis', 'phylesis', 'phyletic', 'phyllite', 'physical', 'phytanes', 'phytonic', 'pianists', 'piasters', 'piastres', 'picachos', 'picaroon', 'piccolos', 'picoline', 'picolins', 'picrates', 'picrites', 'pierrots', 'pietists', 'pilaster', 'pillions', 'pilosity', 'pilsners', 'pinaster', 'pinchers', 'pinholes', 'pinitols', 'pinnaces', 'pinnacle', 'pinochle', 'pinocles', 'pinscher', 'pintails', 'pintanos', 'piracies', 'piscator', 'piscinae', 'piscinal', 'piscinas', 'pisolite', 'pistache', 'pistoles', 'pitchers', 'pitchier', 'pitchily', 'pithiest', 'pithless', 'pitiless', 'pittance', 'plainest', 'plaister', 'plaiters', 'planches', 'planchet', 'planless', 'planners', 'planosol', 'planters', 'plantlet', 'plashers', 'plashier', 'plasters', 'plastery', 'plastics', 'plastron', 'platiest', 'platinic', 'platonic', 'platoons', 'platters', 'playless', 'playlets', 'playlist', 'plectron', 'plenists', 'plethora', 'pliantly', 'pliotron', 'plosions', 'plotless', 'plotline', 'plotters', 'plottier', 'plotties', 'poachers', 'poachier', 'pocosins', 'poetical', 'pointers', 'pointier', 'poisoner', 'poitrels', 'polarise', 'polarity', 'polarons', 'polecats', 'polentas', 'polestar', 'policies', 'polisher', 'polishes', 'politely', 'politest', 'politico', 'politics', 'polities', 'pollices', 'pollinia', 'pollinic', 'pollists', 'pollster', 'poloists', 'poltroon', 'polycots', 'polyenic', 'pontoons', 'ponytail', 'poorness', 'poortith', 'porniest', 'porosity', 'portance', 'portents', 'porthole', 'porticos', 'portions', 'portless', 'portlier', 'portrait', 'portrays', 'portress', 'position', 'positron', 'postally', 'posterns', 'postheat', 'posthole', 'postiche', 'postoral', 'postrace', 'postriot', 'postsync', 'potashes', 'potassic', 'potation', 'potatoes', 'potatory', 'potently', 'potholes', 'potiches', 'potlache', 'potlatch', 'potlines', 'potshots', 'potstone', 'practice', 'practise', 'praetors', 'prairies', 'praisers', 'pralines', 'prancers', 'prattler', 'prattles', 'preallot', 'precasts', 'prechill', 'precinct', 'precools', 'precrash', 'prelatic', 'presorts', 'pretrain', 'pretrial', 'prettily', 'priciest', 'priestly', 'princely', 'princess', 'printers', 'printery', 'priorate', 'prioress', 'priories', 'priority', 'prisoner', 'prissier', 'prissily', 'pristane', 'pristine', 'procaine', 'prochain', 'prochein', 'proctors', 'prolines', 'pronates', 'pronator', 'prorates', 'prosaist', 'prosects', 'prosiest', 'prostate', 'prosties', 'prostyle', 'protases', 'protasis', 'protatic', 'proteans', 'protects', 'proteins', 'protests', 'protists', 'protocol', 'protonic', 'protract', 'protyles', 'psalters', 'psaltery', 'pschents', 'psilocin', 'psilotic', 'psoralen', 'psychics', 'ptyalins', 'pycnoses', 'pycnosis', 'pycnotic', 'pyelitic', 'pyelitis', 'pyorrhea', 'pyranose', 'pyronine', 'pyrostat', 'pyrrhics', 'pyrroles', 'pyrrolic', 'pythonic', 'raccoons', 'rachises', 'rachitic', 'rachitis', 'raciness', 'raillery', 'rainiest', 'rainless', 'raisonne', 'ralliers', 'rallyist', 'ranchero', 'ranchers', 'raptness', 'rarities', 'raspiest', 'ratchets', 'ratholes', 'ratlines', 'ratooner', 'rattlers', 'rattoons', 'reaction', 'reactors', 'realists', 'reallots', 'reanoint', 'reassort', 'recharts', 'recision', 'recitals', 'reclasps', 'recolors', 'rectally', 'relation', 'relators', 'repaints', 'replants', 'replicas', 'replicon', 'repolish', 'reposals', 'reposits', 'reprints', 'reprisal', 'reproach', 'reptilia', 'reschool', 'rescript', 'reshoots', 'resistor', 'resonant', 'resorcin', 'resplits', 'responsa', 'resprays', 'restarts', 'restitch', 'restoral', 'restrain', 'restrict', 'retailor', 'retinals', 'retinols', 'retirant', 'retracts', 'retrains', 'retrally', 'retrials', 'retroact', 'retsinas', 'rheophil', 'rheostat', 'rhetoric', 'rhonchal', 'rhyolite', 'richness', 'ricochet', 'ricottas', 'ripienos', 'ripostes', 'risottos', 'roasters', 'rocaille', 'roiliest', 'roisters', 'roosters', 'rootiest', 'rootless', 'rootlets', 'ropiness', 'rosaries', 'roseolar', 'roseolas', 'roseroot', 'rosinols', 'rosolios', 'rostella', 'rostrate', 'rotaries', 'rotation', 'rotators', 'rotatory', 'rototill', 'rottenly', 'royalist', 'roysters', 'sacristy', 'sailorly', 'salicine', 'salicins', 'saliency', 'salients', 'salinity', 'salliers', 'salterns', 'saltiers', 'saltiest', 'saltines', 'saltires', 'sanction', 'sanctity', 'sanicles', 'sanities', 'sanitise', 'santonin', 'sapiency', 'saponine', 'saponins', 'saponite', 'sartorii', 'satchels', 'satinets', 'satirise', 'satirist', 'scaliest', 'scallion', 'scallops', 'scalpels', 'scalpers', 'scanners', 'scansion', 'scantest', 'scantier', 'scanties', 'scantily', 'scarcely', 'scarcest', 'scarcity', 'scariest', 'scariose', 'scarlets', 'scarpers', 'scatters', 'scattier', 'scenario', 'scenical', 'sceptics', 'sceptral', 'schiller', 'scholars', 'schooner', 'sciatics', 'scilicet', 'sciolist', 'scirocco', 'scolices', 'scollops', 'scoopers', 'scooters', 'scorcher', 'scorches', 'scorners', 'scorpion', 'scotches', 'scotopia', 'scotopic', 'scotties', 'scraichs', 'scrannel', 'scrapers', 'scrapies', 'scratchy', 'scripter', 'scrootch', 'scyphate', 'seaports', 'secantly', 'sections', 'sectoral', 'senators', 'senhoras', 'senility', 'senopias', 'senorita', 'sensilla', 'sensoria', 'septical', 'seraphic', 'seraphin', 'serially', 'sericins', 'serosity', 'serranos', 'settlors', 'shaliest', 'shalloon', 'shallops', 'shallots', 'shannies', 'shanteys', 'shanties', 'shantihs', 'sharpens', 'sharpers', 'sharpest', 'sharpies', 'shatters', 'sheitans', 'shellacs', 'sheroots', 'shiniest', 'shinnery', 'shinneys', 'shinnies', 'shirtier', 'shittahs', 'shittier', 'shoalest', 'shoalier', 'shoehorn', 'shoepacs', 'shooters', 'shophars', 'shortens', 'shortest', 'shortias', 'shorties', 'shortish', 'shrapnel', 'shriller', 'silently', 'silicate', 'silicles', 'silicone', 'silicons', 'silliest', 'siltiest', 'sinister', 'sinopias', 'siphonal', 'siphonic', 'sirenian', 'sirloins', 'siroccos', 'sisterly', 'sitarist', 'slatches', 'slathers', 'slatiest', 'slattern', 'slipcase', 'slipsole', 'slithers', 'slithery', 'slitters', 'sloshier', 'snapshot', 'snarlers', 'snarlier', 'snatcher', 'snatches', 'snitcher', 'snitches', 'snoopers', 'snoopier', 'snoopily', 'snootier', 'snootily', 'snorters', 'snottier', 'snottily', 'soapiest', 'socially', 'societal', 'solacers', 'solanine', 'solanins', 'solarise', 'solation', 'solecist', 'solicits', 'solitary', 'solitons', 'solonets', 'solstice', 'sonances', 'sonantic', 'sonatine', 'sonicate', 'sonorant', 'sonority', 'soothers', 'soothest', 'soothsay', 'sootiest', 'sopranos', 'soricine', 'soroches', 'sororate', 'sorority', 'sorption', 'sorriest', 'spaciest', 'spallers', 'spancels', 'spaniels', 'spanners', 'sparsely', 'sparsity', 'spathose', 'spatters', 'specials', 'spectral', 'spherics', 'spiccato', 'spiciest', 'spillers', 'spinachy', 'spinally', 'spiniest', 'spinners', 'spinnery', 'spinneys', 'spinnies', 'spinster', 'spiracle', 'spirally', 'spirants', 'spiriest', 'spirilla', 'spitters', 'spittles', 'spittoon', 'splasher', 'splatter', 'splenial', 'splicers', 'splinter', 'splitter', 'splotchy', 'spoilers', 'spoliate', 'sponsion', 'spontoon', 'spooneys', 'spoonier', 'spoonies', 'spoonily', 'sporrans', 'sporters', 'sportier', 'sportily', 'spotters', 'spottier', 'spottily', 'sprattle', 'sprayers', 'sprinter', 'stainers', 'staithes', 'stallion', 'stancher', 'stanches', 'stanchly', 'stanhope', 'stanines', 'stannite', 'staplers', 'starches', 'starlets', 'starnose', 'starship', 'starters', 'startler', 'startles', 'statices', 'stations', 'stealths', 'stealthy', 'steapsin', 'stearins', 'stencils', 'stenotic', 'stentors', 'sterical', 'sternson', 'stertors', 'sthenias', 'stiction', 'stillest', 'stillier', 'stinters', 'stipites', 'stitcher', 'stitches', 'stithies', 'stollens', 'stolonic', 'stolport', 'stoniest', 'stoolies', 'stoopers', 'strainer', 'straiten', 'straiter', 'straitly', 'strayers', 'stretchy', 'striates', 'stricter', 'strictly', 'stripers', 'stripier', 'stroller', 'strontia', 'strontic', 'strophes', 'strophic', 'stroyers', 'styliser', 'stylites', 'stylitic', 'styptics', 'syenitic', 'sylphish', 'synanons', 'synaptic', 'syncarps', 'synchros', 'syncline', 'syncopal', 'syncopes', 'syncopic', 'synectic', 'synoptic', 'syntonic', 'syphilis', 'syrphian', 'systolic', 'tachiste', 'tachists', 'tachyons', 'taconite', 'tactions', 'tactless', 'tailless', 'tailspin', 'talipots', 'talliers', 'tallness', 'tallyhos', 'tanistry', 'tapestry', 'tapholes', 'taproots', 'tapsters', 'tarriest', 'tarsiers', 'tartness', 'teashops', 'teaspoon', 'technics', 'tectonic', 'telsonic', 'tenacity', 'tenantry', 'teniasis', 'tennists', 'tenorist', 'tensions', 'teocalli', 'ternions', 'terpinol', 'terrains', 'terrapin', 'tertials', 'tertians', 'tertiary', 'testoons', 'tetanics', 'tetchily', 'tetrarch', 'thatcher', 'thatches', 'thearchy', 'theatric', 'theistic', 'thelitis', 'theocrat', 'theorist', 'theriacs', 'thespian', 'thetical', 'thinners', 'thinness', 'thinnest', 'thinnish', 'thionate', 'thionine', 'thionins', 'thionyls', 'thiophen', 'thiotepa', 'thirster', 'thirties', 'thistles', 'tholepin', 'thoraces', 'thoracic', 'thorites', 'thornier', 'thornily', 'thrasher', 'thrashes', 'thriller', 'throstle', 'tieclasp', 'tillites', 'tinhorns', 'tininess', 'tinniest', 'tinplate', 'tinselly', 'tinstone', 'tintless', 'tintypes', 'tipcarts', 'tipsiest', 'tipsters', 'titaness', 'tithonia', 'toasters', 'toastier', 'toenails', 'toiletry', 'tolerant', 'tonality', 'tonetics', 'tonicity', 'tonishly', 'tonsilar', 'tontines', 'toolless', 'toothier', 'toothily', 'tootlers', 'tootsies', 'topcoats', 'topcross', 'toplines', 'topnotch', 'topsails', 'topsoils', 'topstone', 'torchier', 'torchons', 'tornillo', 'torosity', 'torrents', 'torsions', 'tortilla', 'tortoise', 'tortonis', 'totalise', 'toyshops', 'trachles', 'trachyte', 'tractile', 'traction', 'tractors', 'trailers', 'trainers', 'traipses', 'traitors', 'tranches', 'transect', 'transept', 'tranship', 'transits', 'trapline', 'trapnest', 'trashier', 'trashily', 'treasons', 'trenails', 'triarchy', 'trichina', 'trichite', 'tricolor', 'tricorne', 'tricorns', 'trictrac', 'tricycle', 'triennia', 'triethyl', 'trillers', 'trillion', 'triolets', 'triphase', 'triplane', 'triplets', 'triplite', 'tripolis', 'triposes', 'triptane', 'triptyca', 'triptych', 'trisects', 'tristich', 'tritones', 'trochaic', 'trochars', 'trochili', 'trochils', 'trochlea', 'troilite', 'trollers', 'trolleys', 'trollies', 'trollops', 'trollopy', 'troopers', 'troopial', 'trophies', 'tropical', 'tropines', 'troponin', 'trotline', 'trypsins', 'trysails', 'trysters', 'tylosins', 'typecast', 'typhonic', 'typhoons', 'tyrannic', 'tyrosine', 'yachters']),
]

testing = 'py' if sourcecode.endswith('py') else 'cpp'


FilesNeeded = ['short_wordlist.txt','big_wordlist.txt']

Dir=os.listdir('.')
for fneeded in FilesNeeded:
    if fneeded not in Dir:
        print('getting',fneeded,'from server')
        req = 'http://128.197.128.215:60217/static/content/'+fneeded
        with urllib.request.urlopen(req) as f:
           p = f.read().decode('utf-8')
           g = open(fneeded,'w')
           g.write(p)
           g.close()



# if C++, compile (equalizes for optimization code)
if testing == 'cpp':
    program = sourcecode[:-4]
    T = subprocess.run(['g++', "-std=c++14", "-O3", sourcecode, "-o", program])

    if T.returncode:
        print(T)
        quit()
else:
    program = sourcecode



popen_specs={'stdout':PIPE,'stdin':PIPE,'universal_newlines':True}

def ask_wordplayer(process,case):
    process.stdin.write(case+'\n')
    process.stdin.flush()
    words = []
    while True:
        res=process.stdout.readline()
        if res=='.\n':
            break
        else:
            words.append(res.strip())
    return words

class wordplayerTestCase(unittest.TestCase):
    "short word list tests"
    def setUp(self):
        args = ['python'] if testing=='py' else []
        args += [program,'short_wordlist.txt']
        self.process = subprocess.Popen(args,**popen_specs)
        time.sleep(0.02)
        return_code = self.process.poll()
        if return_code:

            self.fail('Your program exited with return code {}.'.format(return_code))


    def tearDown(self):
        (stdout, stderr) = self.process.communicate('stopthisprogramrightnowplease 0\n',timeout=1)
        self.assertEqual(stdout,'')
        self.assertEqual(stderr,None)


    def test_specs(self):
        "a. answers for short word list"
        for case,answer in Tests_Short:
            with self.subTest(CASE=case):
                words = ask_wordplayer(self.process,case)
                if words != answer:
                    res="Correct: {}, yours: {}".format(answer,words)
                    self.fail(res)


class wordplayerBigTestCase(unittest.TestCase):
    "big word list tests"
    def setUp(self):
        args = ['python'] if testing=='py' else []
        args += [program,'big_wordlist.txt']
        self.process = subprocess.Popen(args,**popen_specs)
        time.sleep(0.02)
        return_code = self.process.poll()
        if return_code:
            self.fail('Your program exited with return code {}.'.format(return_code))


    def tearDown(self):
        (stdout, stderr) = self.process.communicate('done 0\n',timeout=1)
        self.assertEqual(stdout,'')
        self.assertEqual(stderr,None)


    def test_specs(self):
        "a. answers for big word list"
        for case,answer in Tests_Big:
            with self.subTest(CASE=case):
                words = ask_wordplayer(self.process,case)
                if words != answer:
                    res="Correct: {}, yours: {}".format(answer,words)
                    self.fail(res)

    def test_speed(self):
        "b. speed check for big word list"
        print('pausing for 2 seconds for you to process the file')
        time.sleep(2)
        speed_factor=[]
        for target_time, case, answer in Tests_Speed:
            with self.subTest(CASE=case):
                start_time=time.time()
                words = ask_wordplayer(self.process,case)
                duration = (time.time()-start_time)/ slow_factor
                speed_factor.append((case,duration/target_time[testing]))

                if words != answer:
                    res="Correct: {}, yours: {}".format(answer,words)
                    self.fail(res)
        print('Speed test results')
        print('==================')
        print('Time    Case')
        print('------- ----')
        for test,speed in speed_factor:
            print("{:7.5f}".format(speed),test)

        total_score = sum(x[1] for x in speed_factor)
        print('total time: {:5.3f}'.format(total_score))
        if total_score>10:
            self.fail('Your total relative time to run the speed tests was {}. Our time is about 6.'.format(total_score))


st = time.time()
D = {}
for k in range(10000):
    D[k] = random.randint(1,100)
en = time.time()
slow_factor = (en-st)/0.02
print('slow factor for your computer:',slow_factor)


def run_test(name,testcase):
    print('running the {} test'.format(name),end=' ')
    results = unittest.result.TestResult()
    unittest.loader.TestLoader().loadTestsFromTestCase(testcase).run(results)
    passed = results.wasSuccessful()
    print('...passed.' if passed else "...failed.")
    return passed

if __name__ == '__main__':
    passed_spec = run_test('spec',wordplayerTestCase)
    passed_speed = run_test('speed',wordplayerBigTestCase)





