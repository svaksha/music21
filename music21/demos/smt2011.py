#-------------------------------------------------------------------------------
# Name:         smt2011.py
# Purpose:      Demonstrations for the SMT 2011 poster session
#
# Authors:      Christopher Ariza
#               Michael Scott Cuthbert
#
# Copyright:    (c) 2009-2010 The music21 Project
# License:      LGPL
#-------------------------------------------------------------------------------






import unittest, doctest
from music21 import *

_MOD = 'demo/smt2010.py'
environLocal = environment.Environment(_MOD)




#-------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def runTest(self):
        '''
        '''
        pass
    


    def testEx01(self):
        # Basic operations for creating and manipulating scales.

        sc1 = scale.MajorScale('a-')

        # get pitches from any range of this scale
        print(sc1.getPitches('g2', 'c4'))
        self.assertEqual(str(sc1.getPitches('g2', 'c4')), 
        '[G2, A-2, B-2, C3, D-3, E-3, F3, G3, A-3, B-3, C4]')

        # get a scale degree from a pitch
        print(sc1.getScaleDegreeFromPitch('b-'))
        self.assertEqual(sc1.getScaleDegreeFromPitch('b-'), 2)

        # what is the scale degree of the pitch in relative minor
        print(str(sc1.getRelativeMinor().getScaleDegreeFromPitch('b-')))
        self.assertEqual(sc1.getRelativeMinor().getScaleDegreeFromPitch('b-'), 4)

        # given a pitch in this scale, what is the next pitch
        print(sc1.next('g2', 'ascending'))
        self.assertEqual(str(sc1.next('g2', 'ascending')), 'A-2')

        # descending three scale steps
        print(sc1.next('g2', 'descending', 3))
        self.assertEqual(str(sc1.next('g2', 'descending', 3)), 'D-2')


        # derive a new major scale based on a pitch for a scale degree
        print(sc1.deriveByDegree(7, 'f#4').pitches)
        self.assertEqual(str(sc1.deriveByDegree(7, 'f#4').pitches), 
            '[G3, A3, B3, C4, D4, E4, F#4, G4]')


        # a whole tone scale
        sc2 = scale.WholeToneScale('f#')

        # get pitches from any range of this scale
        print str(sc2.getPitches('g2', 'c4'))
        self.assertEqual(str(sc2.getPitches('g2', 'c4')), 
        '[A-2, B-2, C3, D3, F-3, G-3, A-3, B-3, C4]')

            # get a scale degree from a pitch
        print(str(sc2.getScaleDegreeFromPitch('e')))
        self.assertEqual(sc2.getScaleDegreeFromPitch('e'), 6)

        # given a pitch in this scale, what is the next pitch
        print(sc2.next('d4', 'ascending'))
        self.assertEqual(str(sc2.next('d4', 'ascending')), 'E4')


        # transpose the scale
        print(sc2.transpose('m2').pitches)
        self.assertEqual(str(sc2.transpose('m2').pitches), '[G4, A4, B4, C#5, D#5, E#5, G5]')

        # get as a chord and get its forte class
        self.assertEqual(sc2.transpose('m2').chord.forteClass, '6-35')



    def testEx02(self): 
        # Labeling a vocal part based on scale degrees derived from key signature and from a specified target key.

        s = corpus.parseWork('hwv56/movement3-03.md')#.measures(1,7)
        basso = s.parts['basso']
        s.remove(basso)
        
        ksScale = s.flat.getElementsByClass('KeySignature')[0].getScale()
        targetScale = scale.MajorScale('A')
        for n in basso.flat.getElementsByClass('Note'):
            # get the scale degree from this pitch
            n.addLyric(ksScale.getScaleDegreeFromPitch(n.pitch))
            n.addLyric(targetScale.getScaleDegreeFromPitch(n.pitch))
        
        reduction = s.chordify()
        for c in reduction.flat.getElementsByClass('Chord'):
            c.closedPosition(forceOctave=4, inPlace=True)
            c.removeRedundantPitches(inPlace=True)
        
        
        display = stream.Score()
        display.insert(0, basso)
        display.insert(0, reduction)
        #display.show()




    def testEx03(self):

        # What is the most common closing soprano scale degree by key signature
        # in the bach chorales?
        from music21 import graph

        results = {}
        for fn in corpus.bachChorales[:2]:
            s = corpus.parseWork(fn)
            ksScale = s.flat.getElementsByClass('KeySignature')[0].getScale()
            for p in s.parts:
                if p.id.lower() == 'soprano':
                    n = s.parts['soprano'].flat.getElementsByClass('Note')[-1]
                    degree = ksScale.getScaleDegreeFromPitch(n.pitch)
                    if degree not in results.keys():
                        results[degree] = 0
                    results[degree] += 1
        print(results)

        # Results for all Bach chorales
        #{1: 307, 2: 3, 3: 11, 4: 31, 5: 34, 6: 5, 7: 2, None: 3}

        #g = graph.GraphHistogram()
        #g.setData([(x, y) for x, y in sorted(results.items())])
        #g.process()

    def xtestEx04(self):
        # what

        scSrc = scale.MajorScale()

        niederlande = corpus.search('niederlande', 'locale')

        results = {}
        for name, group in [('niederlande', niederlande)]:
            workCount = 0

            for fp, n in group:
                workCount += 1
    
                s = converter.parse(fp, number=n)
    
                # derive a best-fit concrete major scale
                scFound = scSrc.derive(s)

                # if we find a scale with no unmatched pitches
                if len(scFound.match(s)['notMatched']) == 0:
                    # find out what pitches in major scale are not used
                    post = scFound.findMissing(s)
                    for p in post:
                        degree = scFound.getScaleDegreeFromPitch(p)
                        if degree not in results.keys():
                            results[degree] = 0
                        results[degree] += 1

        print ('Of %s works, the following major scale degrees are not used the the following number of times:' % workCount)
        print results

        #Of 104 works, the following major scale degrees are not used the the following number of times:
        #{4: 5, 5: 1, 6: 6, 7: 6}



if __name__ == "__main__":
    import music21
    import sys

    if len(sys.argv) == 1: # normal conditions
        music21.mainTest(Test)

    elif len(sys.argv) > 1:
        t = Test()
        #t.testEx02()
        t.testEx03()
        #t.testEx04()


#------------------------------------------------------------------------------
# eof

