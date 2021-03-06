from music21 import corpus
import unittest
import re

class Test(unittest.TestCase):

    def runTest(self):
        pass

    def testGetPaths(self):
        for known in ['haydn/opus74no2/movement4.mxl',
            'beethoven/opus18no3.mxl',
            'beethoven/opus59no1/movement2.mxl',
            'mozart/k80/movement4.mxl',
            'schumann/opus41no1/movement5.mxl',
            ]:
            a = corpus.getWork(known)
            # make sure it is not an empty list
            self.assertNotEqual(len(a), 0)
            workSlashes = re.sub(r'\\', '/', a)
            self.assertEqual(workSlashes.endswith(known), True)

    def testBachKeys(self):
        from music21 import key
        keyObjs = []
        for filePath in corpus.getComposer('bach')[23:28]: # get 5 in the middle
            s = corpus.parse(filePath)
            # get keys from first part
            keyStream = s.parts[0].flat.getElementsByClass(key.KeySignature)
            keyObj = keyStream[0]
            keyObjs.append(keyObj)
            #environLocal.printDebug([keyObj])
        self.assertEqual(len(keyObjs), 5)

    def testEssenImport(self):
        # can get a single file just by file name
        filePath = corpus.getWork('altdeu10')
        self.assertTrue(filePath.endswith('essenFolksong/altdeu10.abc') or
            filePath.endswith(r'essenFolksong\altdeu10.abc'))
        filePathCollection = corpus.getComposer('essenFolksong')
        self.assertEqual(len(filePathCollection), 31)
        filePathCollection = corpus.getComposer('essenFolksong', ['abc'])
        self.assertEqual(len(filePathCollection), 31)

    def testDesPrezImport(self):
        # can get a single file just by file name
        filePath = corpus.getWork('fortunaDunGranTempo')
        filePath = re.sub(r'\\', '/', filePath)
        self.assertEqual(filePath.endswith(
            'josquin/fortunaDunGranTempo.abc'), True)
        filePathCollection = corpus.getComposer('josquin')
        self.assertEqual(len(filePathCollection) >= 8, True)
        filePathCollection = corpus.getComposer('josquin', ['abc'])
        self.assertEqual(len(filePathCollection) >= 8, True)

    def testHandelImport(self):
        # can get a single file just by file name
        unused_fp = corpus.getWork('hwv56/movement1-01')#
        fpCollection = corpus.getComposer('handel')
        self.assertEqual(len(fpCollection) >= 1, True)
        fpCollection = corpus.getComposer('handel', ['md'])
        self.assertEqual(len(fpCollection) >= 1, True)

    def testSearch01(self):
        searchResults = corpus.search('china', field='locale')
        self.assertEqual(len(searchResults) > 1200, True)

    def testSearch02(self):
        searchResults = corpus.search('Sichuan', field='locale')
        self.assertEqual(len(searchResults), 47)

    def testSearch03(self):
        searchResults = corpus.search('Taiwan', field='locale')
        self.assertEqual(len(searchResults), 27)
        pathInfo = sorted((searchResult.sourcePath, searchResult.number)
            for searchResult in searchResults)
        self.assertEqual(pathInfo, [
            (u'essenFolksong/han1.abc', u'269'),
            (u'essenFolksong/han1.abc', u'270'),
            (u'essenFolksong/han1.abc', u'271'),
            (u'essenFolksong/han1.abc', u'272'),
            (u'essenFolksong/han1.abc', u'273'),
            (u'essenFolksong/han1.abc', u'274'),
            (u'essenFolksong/han1.abc', u'335'),
            (u'essenFolksong/han1.abc', u'528'),
            (u'essenFolksong/han1.abc', u'529'),
            (u'essenFolksong/han1.abc', u'530'),
            (u'essenFolksong/han2.abc', u'204'),
            (u'essenFolksong/han2.abc', u'205'),
            (u'essenFolksong/han2.abc', u'206'),
            (u'essenFolksong/han2.abc', u'207'),
            (u'essenFolksong/han2.abc', u'208'),
            (u'essenFolksong/han2.abc', u'209'),
            (u'essenFolksong/han2.abc', u'210'),
            (u'essenFolksong/han2.abc', u'211'),
            (u'essenFolksong/han2.abc', u'212'),
            (u'essenFolksong/han2.abc', u'213'),
            (u'essenFolksong/han2.abc', u'214'),
            (u'essenFolksong/han2.abc', u'215'),
            (u'essenFolksong/han2.abc', u'216'),
            (u'essenFolksong/han2.abc', u'217'),
            (u'essenFolksong/han2.abc', u'218'),
            (u'essenFolksong/han2.abc', u'219'),
            (u'essenFolksong/han2.abc', u'220'),
            ])

    def testSearch04(self):
        searchResults = corpus.search('Sichuan|Taiwan', field='locale')
        self.assertEqual(len(searchResults), 74)

    def testSearch05(self):
        searchResults = corpus.search('bach')
        self.assertEqual(len(searchResults) > 120, True)

    def testSearch06(self):
        searchResults = corpus.search('haydn', field='composer')
        self.assertEqual(len(searchResults), 0)
        searchResults = corpus.search('haydn|beethoven', field='composer')
        self.assertEqual(len(searchResults) >= 16, True)

    def testSearch07(self):
        searchResults = corpus.search('canon')
        self.assertEqual(len(searchResults) >= 1, True)

    def testSearch08(self):
        searchResults = corpus.search('3/8', field='timeSignature')
        self.assertEqual(len(searchResults) > 360, True)

    def testSearch09(self):
        searchResults = corpus.search('3/.', field='timeSignature')
        self.assertEqual(len(searchResults) >= 2200 , True)

    def testSearch10(self):
        from music21 import key
        ks = key.KeySignature(3, 'major')
        searchResults = corpus.search(str(ks), field='keySignature')
        self.assertEqual(len(searchResults) >= 32, True, len(searchResults))

    def testSearch11(self):
        searchResults = corpus.search('mode phry(.*)', field='keySignature')
        self.assertEqual(len(searchResults) >= 9, True)

    def testSearch12(self):
        # searching virtual entries
        searchResults = corpus.search('coltrane', field='composer')
        self.assertEqual(len(searchResults) > 0, True)
        # returns items in pairs: url and work number
        self.assertEqual(searchResults[0].sourcePath,
            'http://static.wikifonia.org/1164/musicxml.mxl')

    def testGetWorkList(self):
        self.assertEqual(len(corpus.getPaths('.md')) >= 38, True)
        workList = corpus.getWorkList('bach/artOfFugue_bwv1080', 1, '.zip')
        self.assertEqual(len(workList), 1)
        self.assertEqual(len(corpus.getWorkList('handel/hwv56', (1, 1), '.md')), 1)
        self.assertEqual(len(corpus.getWorkList('handel/hwv56', '1-01', '.md')), 1)
        self.assertEqual(len(corpus.getWorkList('bach/artOfFugue_bwv1080')), 21)
        self.assertEqual(len(corpus.getWorkList('bach/artOfFugue_bwv1080', 1)), 1)

        # there are two versions of this file
        self.assertEqual(len(corpus.getWorkList('beethoven/opus18no1', 1)), 2)

        # if specify movement
        for bwv in [
            'bwv846', 'bwv847', 'bwv848', 'bwv849', 'bwv850', 'bwv851',
            'bwv852', 'bwv853', 'bwv854', 'bwv855', 'bwv856', 'bwv857',
            'bwv858', 'bwv859', 'bwv860', 'bwv861', 'bwv862', 'bwv863',
            'bwv864', 'bwv865', 'bwv866', 'bwv867', 'bwv868', 'bwv869',
            'bwv870', 'bwv871', 'bwv872', 'bwv873', 'bwv874', 'bwv875',
            'bwv876', 'bwv877', 'bwv878', 'bwv879', 'bwv880', 'bwv881',
            'bwv882', 'bwv883', 'bwv884', 'bwv885', 'bwv886', 'bwv887',
            'bwv888', 'bwv889', 'bwv890', 'bwv891', 'bwv892', 'bwv893',
            ]:
            #print bwv
            self.assertEqual(len(corpus.getWorkList(bwv)), 2)
            self.assertEqual(len(corpus.getWorkList(bwv, 1)), 1)
            self.assertEqual(len(corpus.getWorkList(bwv, 2)), 1)

    def testWTCImport01(self):
        score = corpus.parse('bach/bwv846', 1)
        self.assertEqual(
            score.metadata.title,
            'WTC I: Prelude and Fugue in C major',
            )
        self.assertEqual(score.metadata.movementNumber, '1')

    def testWTCImport02(self):
        score = corpus.parse('bach/bwv846', 2)
        self.assertEqual(score.metadata.movementName, 'Fugue  I. ')
        self.assertEqual(score.metadata.movementNumber, '2')

    def testWTCImport03(self):
        score = corpus.parse('bach/bwv862', 1)
        self.assertEqual(
            score.metadata.title,
            'WTC I: Prelude and Fugue in A flat major',
            )

    def testWTCImport04(self):
        score = corpus.parse('bach/bwv888', 1)
        self.assertEqual(
            score.metadata.title,
            'WTC II: Prelude and Fugue in A major',
            )
        #s.show()

#     def testWorkReferences(self):
#         s = corpus.getWorkReferences()
#
#         # presenly 19 top level lists
#         self.assertEqual(len(s)>=19, True)
#         self.assertEqual(len(s[0].keys()), 4)

if __name__ == "__main__":
    import music21
    music21.mainTest('noDocTest',Test)


#------------------------------------------------------------------------------
# eof
