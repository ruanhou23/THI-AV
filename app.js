/**
 * TOEIC MASTER - MAIN APPLICATION SCRIPT
 * Comprehensive TOEIC Exam & Practice Simulator:
 * 1. TOEIC Listening (Test 1 - 4: 280 questions, 176 audios, 24 images)
 * 2. TOEIC Reading B1 (Test 1 - 4: 200 questions, passages, complete sentences)
 * 3. Sentence Translation Practice (480 bilingual questions with vocabulary & grammar)
 * 4. Automatic Grading, TOEIC Scaled Score (5-495), Detailed Review
 * 5. Offline-ready, Dark/Light Theme & Keyboard Shortcuts
 */

(function () {
  'use strict';

  // Application State
  const state = {
    // Current Active Screen: 'home' | 'exam' | 'score' | 'translation'
    activeScreen: 'home',

    // Current Skill: 'listening' | 'reading'
    currentSkill: 'listening',

    // Exam / Practice Mode
    mode: 'exam', // 'exam' or 'practice'
    testId: 1,    // 1, 2, 3, 4 or 'part_1', 'part_2', 'part_3'
    questions: [],
    currentIndex: 0,
    userAnswers: {},     // { questionId: "A" }
    flaggedQuestions: {},// { questionId: true }
    timerSeconds: 45 * 60,
    timerInterval: null,
    timeSpentSeconds: 0,
    filterReview: 'all', // 'all', 'wrong', 'right', 'unanswered'
    theme: localStorage.getItem('toeic_theme') || 'dark',

    // Translation Practice State
    transDirection: 'en-vi', // 'en-vi' or 'vi-en'
    transSkill: 'all',       // 'all', 'listening', 'reading'
    transTest: 'all',
    transPart: 'all',
    transQuestions: [],
    transIndex: 0,
    transRatings: JSON.parse(localStorage.getItem('toeic_trans_ratings') || '{}'),

    // Writing Practice State
    writingSubtab: 'paragraph', // 'paragraph' or 'qa'
    writingParagraphIndex: 0,
    writingParagraphDrafts: JSON.parse(localStorage.getItem('toeic_writing_para_drafts') || '{}'),
    writingQACategory: 'all',
    writingQAIndex: 0,
    writingQADrafts: JSON.parse(localStorage.getItem('toeic_writing_qa_drafts') || '{}'),
    writingStructureOpen: true,

    // Question Editor State
    customOverrides: JSON.parse(localStorage.getItem('toeic_custom_overrides') || '{}'),
    editorSearchQuery: '',
    editorFilterSkill: 'all',
    editorFilterTest: 'all',
    editorFilterPart: 'all',
    editorFilterEdited: 'all',
    editorVisibleLimit: 20,
    editorFilteredQuestions: [],

    // Reading Shuffle Options Mode
    readingShuffle: localStorage.getItem('toeic_reading_shuffle') !== 'false',

    // Listening Hide Text Mode (Only show A B C D)
    listeningHideText: localStorage.getItem('toeic_listening_hide_text') === 'true',
    listeningPeekQuestionId: null,

    // Pre-test setup
    preTestTarget: null,

    // Speaking Study & LAN State
    speakingSubtab: 'study',
    speakingP1TopicId: 'tech',
    speakingP1QIndex: 0,
    speakingShowSampleP1: false,
    speakingP2TopicIndex: 0,
    speakingShowSampleP2: false,
    speakingExamType: 'full',
    speakingStudyFilter: 'all',
    speakingStudySearch: '',
    speakingStudySpeed: 0.95,
    speakingStudyShowVi: true,
    lanUrl: 'http://192.168.2.6:8000/index.html'
  };

  // DOM Elements Cache
  const el = {
    // Screens
    screenHome: document.getElementById('screenHome'),
    screenExam: document.getElementById('screenExam'),
    screenScore: document.getElementById('screenScore'),
    screenTranslation: document.getElementById('screenTranslation'),
    screenWriting: document.getElementById('screenWriting'),

    // Nav
    tabNavListening: document.getElementById('tabNavListening'),
    tabNavReading: document.getElementById('tabNavReading'),
    tabNavTranslation: document.getElementById('tabNavTranslation'),
    tabNavWriting: document.getElementById('tabNavWriting'),
    navCenterInfo: document.getElementById('navCenterInfo'),
    currentTestDisplay: document.getElementById('currentTestDisplay'),
    currentModeDisplay: document.getElementById('currentModeDisplay'),
    timerCountdown: document.getElementById('timerCountdown'),
    btnThemeToggle: document.getElementById('btnThemeToggle'),
    themeIcon: document.getElementById('themeIcon'),
    btnExitTest: document.getElementById('btnExitTest'),
    btnTopSubmit: document.getElementById('btnTopSubmit'),

    // Home Skill Toggles
    skillToggleListening: document.getElementById('skillToggleListening'),
    skillToggleReading: document.getElementById('skillToggleReading'),
    testSectionTitle: document.getElementById('testSectionTitle'),
    readingShuffleToggleWrap: document.getElementById('readingShuffleToggleWrap'),
    chkReadingShuffle: document.getElementById('chkReadingShuffle'),
    listeningHideToggleWrap: document.getElementById('listeningHideToggleWrap'),
    chkListeningHide: document.getElementById('chkListeningHide'),
    testsGridContainer: document.getElementById('testsGridContainer'),
    partPracticeTitle: document.getElementById('partPracticeTitle'),
    partPracticeSub: document.getElementById('partPracticeSub'),
    partButtonsGroup: document.getElementById('partButtonsGroup'),

    // Home Modes
    modeCardStudy: document.getElementById('modeCardStudy'),
    modeCardExam: document.getElementById('modeCardExam'),
    modeCardPractice: document.getElementById('modeCardPractice'),
    modeCardTranslation: document.getElementById('modeCardTranslation'),
    modeCardWriting: document.getElementById('modeCardWriting'),

    // Exam Workspace Audio Player
    questionAudioBar: document.getElementById('questionAudioBar'),
    audioPlayer: document.getElementById('questionAudioPlayer'),
    currentAudioLabel: document.getElementById('currentAudioLabel'),
    btnAudioPlayPause: document.getElementById('btnAudioPlayPause'),
    playPauseIcon: document.getElementById('playPauseIcon'),
    btnAudioRewind: document.getElementById('btnAudioRewind'),
    btnAudioForward: document.getElementById('btnAudioForward'),
    audioSeekBar: document.getElementById('audioSeekBar'),
    audioCurrentTime: document.getElementById('audioCurrentTime'),
    audioTotalDuration: document.getElementById('audioTotalDuration'),
    audioSpeedSelect: document.getElementById('audioSpeedSelect'),
    audioWaveAnim: document.querySelector('.audio-wave-anim'),

    // Question Detail
    qNumberPill: document.getElementById('qNumberPill'),
    qPartPill: document.getElementById('qPartPill'),
    qSkillPill: document.getElementById('qSkillPill'),
    qShufflePill: document.getElementById('qShufflePill'),
    btnFlagQuestion: document.getElementById('btnFlagQuestion'),
    flagBtnText: document.getElementById('flagBtnText'),
    qPassageContainer: document.getElementById('qPassageContainer'),
    qPassageContent: document.getElementById('qPassageContent'),
    qImageContainer: document.getElementById('qImageContainer'),
    qImage: document.getElementById('qImage'),
    qPrompt: document.getElementById('qPrompt'),
    qOptionsContainer: document.getElementById('qOptionsContainer'),
    qExplanationBox: document.getElementById('qExplanationBox'),
    qExplanationContent: document.getElementById('qExplanationContent'),
    btnPrevQuestion: document.getElementById('btnPrevQuestion'),
    btnNextQuestion: document.getElementById('btnNextQuestion'),
    answeredCounterText: document.getElementById('answeredCounterText'),

    // Palette
    titleGroupPart1: document.getElementById('titleGroupPart1'),
    titleGroupPart2: document.getElementById('titleGroupPart2'),
    titleGroupPart3: document.getElementById('titleGroupPart3'),
    gridPart1: document.getElementById('gridPart1'),
    gridPart2: document.getElementById('gridPart2'),
    gridPart3: document.getElementById('gridPart3'),
    btnSubmitExam: document.getElementById('btnSubmitExam'),

    // Score Report
    scoreEstimated: document.getElementById('scoreEstimated'),
    scoreTitle: document.getElementById('scoreTitle'),
    scoreSubText: document.getElementById('scoreSubText'),
    correctCountDisplay: document.getElementById('correctCountDisplay'),
    accuracyPercentage: document.getElementById('accuracyPercentage'),
    timeSpentDisplay: document.getElementById('timeSpentDisplay'),
    bPart1Label: document.getElementById('bPart1Label'),
    bPart1Sub: document.getElementById('bPart1Sub'),
    p1ScoreText: document.getElementById('p1ScoreText'),
    p1BarFill: document.getElementById('p1BarFill'),
    bPart2Label: document.getElementById('bPart2Label'),
    bPart2Sub: document.getElementById('bPart2Sub'),
    p2ScoreText: document.getElementById('p2ScoreText'),
    p2BarFill: document.getElementById('p2BarFill'),
    bPart3Label: document.getElementById('bPart3Label'),
    bPart3Sub: document.getElementById('bPart3Sub'),
    p3ScoreText: document.getElementById('p3ScoreText'),
    p3BarFill: document.getElementById('p3BarFill'),
    cntFilterAll: document.getElementById('cntFilterAll'),
    cntFilterWrong: document.getElementById('cntFilterWrong'),
    cntFilterRight: document.getElementById('cntFilterRight'),
    cntFilterUnanswered: document.getElementById('cntFilterUnanswered'),
    reviewQuestionsList: document.getElementById('reviewQuestionsList'),
    btnRetakeTest: document.getElementById('btnRetakeTest'),
    btnChooseAnotherTest: document.getElementById('btnChooseAnotherTest'),

    // Modal
    confirmModal: document.getElementById('confirmModal'),
    modalWarningText: document.getElementById('modalWarningText'),
    btnCancelSubmit: document.getElementById('btnCancelSubmit'),
    btnConfirmSubmit: document.getElementById('btnConfirmSubmit'),

    // Pre-test Setup Modal
    preTestModal: document.getElementById('preTestModal'),
    preTestIcon: document.getElementById('preTestIcon'),
    preTestTitle: document.getElementById('preTestTitle'),
    preTestDesc: document.getElementById('preTestDesc'),
    preTestModeStudy: document.getElementById('preTestModeStudy'),
    preTestModeExam: document.getElementById('preTestModeExam'),
    preTestModePractice: document.getElementById('preTestModePractice'),
    preTestShuffleRow: document.getElementById('preTestShuffleRow'),
    chkPreTestShuffle: document.getElementById('chkPreTestShuffle'),
    btnCancelPreTest: document.getElementById('btnCancelPreTest'),
    btnConfirmStartTest: document.getElementById('btnConfirmStartTest'),
    btnToggleShuffleInExam: document.getElementById('btnToggleShuffleInExam'),
    shuffleBtnText: document.getElementById('shuffleBtnText'),
    preTestListeningHideRow: document.getElementById('preTestListeningHideRow'),
    chkPreTestListeningHide: document.getElementById('chkPreTestListeningHide'),
    btnToggleListeningHideInExam: document.getElementById('btnToggleListeningHideInExam'),
    listeningHideIcon: document.getElementById('listeningHideIcon'),
    listeningHideLabel: document.getElementById('listeningHideLabel'),
    listeningHideBanner: document.getElementById('listeningHideBanner'),
    btnPeekListening: document.getElementById('btnPeekListening'),
    studyModeBanner: document.getElementById('studyModeBanner'),
    btnStudyToExam: document.getElementById('btnStudyToExam'),

    // Translation Screen Elements
    btnDirEnVi: document.getElementById('btnDirEnVi'),
    btnDirViEn: document.getElementById('btnDirViEn'),
    transSelectSkill: document.getElementById('transSelectSkill'),
    transSelectTest: document.getElementById('transSelectTest'),
    transSelectPart: document.getElementById('transSelectPart'),
    transNumberPill: document.getElementById('transNumberPill'),
    transPartPill: document.getElementById('transPartPill'),
    transContextPill: document.getElementById('transContextPill'),
    btnTransAudioPlay: document.getElementById('btnTransAudioPlay'),
    transAudioSpeed: document.getElementById('transAudioSpeed'),
    transImageContainer: document.getElementById('transImageContainer'),
    transImage: document.getElementById('transImage'),
    transSourceLabel: document.getElementById('transSourceLabel'),
    transSourceText: document.getElementById('transSourceText'),
    transUserInput: document.getElementById('transUserInput'),
    transHintBox: document.getElementById('transHintBox'),
    transHintKeywords: document.getElementById('transHintKeywords'),
    btnToggleHint: document.getElementById('btnToggleHint'),
    btnRevealTranslation: document.getElementById('btnRevealTranslation'),
    transRevealBox: document.getElementById('transRevealBox'),
    transTargetLabel: document.getElementById('transTargetLabel'),
    transTargetText: document.getElementById('transTargetText'),
    transVocabSection: document.getElementById('transVocabSection'),
    transVocabChips: document.getElementById('transVocabChips'),
    transGrammarSection: document.getElementById('transGrammarSection'),
    transGrammarContent: document.getElementById('transGrammarContent'),
    btnTransPrev: document.getElementById('btnTransPrev'),
    btnTransNext: document.getElementById('btnTransNext'),
    transProgressText: document.getElementById('transProgressText'),
    transPaletteGrid: document.getElementById('transPaletteGrid'),
    btnResetTransProgress: document.getElementById('btnResetTransProgress'),

    // Writing Mode Elements
    btnWritingSubtabParagraph: document.getElementById('btnWritingSubtabParagraph'),
    btnWritingSubtabQA: document.getElementById('btnWritingSubtabQA'),
    writingAutosaveIndicator: document.getElementById('writingAutosaveIndicator'),
    btnWritingClearDraft: document.getElementById('btnWritingClearDraft'),
    viewWritingParagraph: document.getElementById('viewWritingParagraph'),
    viewWritingQA: document.getElementById('viewWritingQA'),
    paragraphTopicSelector: document.getElementById('paragraphTopicSelector'),
    paragraphTargetBadge: document.getElementById('paragraphTargetBadge'),
    btnSpeakSampleParaPrompt: document.getElementById('btnSpeakSampleParaPrompt'),
    paragraphPromptTitle: document.getElementById('paragraphPromptTitle'),
    paragraphPromptVi: document.getElementById('paragraphPromptVi'),
    btnToggleStructure: document.getElementById('btnToggleStructure'),
    structureToggleIcon: document.getElementById('structureToggleIcon'),
    structureBodyContent: document.getElementById('structureBodyContent'),
    outlineOpeningText: document.getElementById('outlineOpeningText'),
    outlineBodyText: document.getElementById('outlineBodyText'),
    outlineConclusionText: document.getElementById('outlineConclusionText'),
    paragraphConnectorsList: document.getElementById('paragraphConnectorsList'),
    paragraphVocabList: document.getElementById('paragraphVocabList'),
    paraWordCountBadge: document.getElementById('paraWordCountBadge'),
    paraCharCountBadge: document.getElementById('paraCharCountBadge'),
    paraStatusBadge: document.getElementById('paraStatusBadge'),
    paragraphTextarea: document.getElementById('paragraphTextarea'),
    btnSpeakUserParagraph: document.getElementById('btnSpeakUserParagraph'),
    btnRevealParagraphSample: document.getElementById('btnRevealParagraphSample'),
    paragraphSampleReveal: document.getElementById('paragraphSampleReveal'),
    sampleParaWordCountPill: document.getElementById('sampleParaWordCountPill'),
    btnSpeakSampleParagraph: document.getElementById('btnSpeakSampleParagraph'),
    sampleParaEnBox: document.getElementById('sampleParaEnBox'),
    sampleParaViBox: document.getElementById('sampleParaViBox'),
    sampleParaVocabGrid: document.getElementById('sampleParaVocabGrid'),
    paragraphComparisonBox: document.getElementById('paragraphComparisonBox'),
    qaCategoryNav: document.getElementById('qaCategoryNav'),
    qaNumberPill: document.getElementById('qaNumberPill'),
    qaThemePill: document.getElementById('qaThemePill'),
    qaStatusPill: document.getElementById('qaStatusPill'),
    btnSpeakQAQuestion: document.getElementById('btnSpeakQAQuestion'),
    qaPromptEn: document.getElementById('qaPromptEn'),
    qaPromptVi: document.getElementById('qaPromptVi'),
    qaStarterChipsList: document.getElementById('qaStarterChipsList'),
    qaKeywordChipsList: document.getElementById('qaKeywordChipsList'),
    qaWordCountBadge: document.getElementById('qaWordCountBadge'),
    qaAnswerTextarea: document.getElementById('qaAnswerTextarea'),
    btnSpeakUserQA: document.getElementById('btnSpeakUserQA'),
    btnRevealQASample: document.getElementById('btnRevealQASample'),
    qaSampleReveal: document.getElementById('qaSampleReveal'),
    btnSpeakQASample: document.getElementById('btnSpeakQASample'),
    qaSampleEnBox: document.getElementById('qaSampleEnBox'),
    qaSampleViBox: document.getElementById('qaSampleViBox'),
    qaComparisonBox: document.getElementById('qaComparisonBox'),
    btnQAPrev: document.getElementById('btnQAPrev'),
    btnQANext: document.getElementById('btnQANext'),
    qaProgressSummary: document.getElementById('qaProgressSummary'),
    writingPaletteTitle: document.getElementById('writingPaletteTitle'),
    writingPaletteGrid: document.getElementById('writingPaletteGrid'),
    btnResetAllWritingDrafts: document.getElementById('btnResetAllWritingDrafts'),

    // Question Editor Elements
    screenEditor: document.getElementById('screenEditor'),
    tabNavEditor: document.getElementById('tabNavEditor'),
    modeCardEditor: document.getElementById('modeCardEditor'),
    editorSearchInput: document.getElementById('editorSearchInput'),
    btnClearEditorSearch: document.getElementById('btnClearEditorSearch'),
    editorFilterSkill: document.getElementById('editorFilterSkill'),
    editorFilterTest: document.getElementById('editorFilterTest'),
    editorFilterPart: document.getElementById('editorFilterPart'),
    editorFilterEdited: document.getElementById('editorFilterEdited'),
    editorResultsCount: document.getElementById('editorResultsCount'),
    editorEditedCountBadge: document.getElementById('editorEditedCountBadge'),
    editorQuestionsContainer: document.getElementById('editorQuestionsContainer'),
    editorPaginationBar: document.getElementById('editorPaginationBar'),
    btnEditorLoadMore: document.getElementById('btnEditorLoadMore'),
    btnExportCustomData: document.getElementById('btnExportCustomData'),
    btnResetAllOverrides: document.getElementById('btnResetAllOverrides'),

    // Speaking Module Elements
    screenSpeaking: document.getElementById('screenSpeaking'),
    tabNavSpeaking: document.getElementById('tabNavSpeaking'),
    modeCardSpeaking: document.getElementById('modeCardSpeaking'),
    speakingStatusBadge: document.getElementById('speakingStatusBadge'),
    btnSpeakingStopAllAudio: document.getElementById('btnSpeakingStopAllAudio'),
    btnSpeakingSubtabPart1: document.getElementById('btnSpeakingSubtabPart1'),
    btnSpeakingSubtabPart2: document.getElementById('btnSpeakingSubtabPart2'),
    btnSpeakingSubtabExam: document.getElementById('btnSpeakingSubtabExam'),
    viewSpeakingPart1: document.getElementById('viewSpeakingPart1'),
    viewSpeakingPart2: document.getElementById('viewSpeakingPart2'),
    viewSpeakingExam: document.getElementById('viewSpeakingExam'),
    // Part 1
    speakingP1TopicSelector: document.getElementById('speakingP1TopicSelector'),
    speakingP1TopicBadge: document.getElementById('speakingP1TopicBadge'),
    speakingP1QNumBadge: document.getElementById('speakingP1QNumBadge'),
    btnP1ListenQuestion: document.getElementById('btnP1ListenQuestion'),
    speakingP1QuestionText: document.getElementById('speakingP1QuestionText'),
    speakingP1QuestionVi: document.getElementById('speakingP1QuestionVi'),
    btnP1RecordToggle: document.getElementById('btnP1RecordToggle'),
    p1RecordBtnText: document.getElementById('p1RecordBtnText'),
    p1RecordTimer: document.getElementById('p1RecordTimer'),
    p1RecordTimerText: document.getElementById('p1RecordTimerText'),
    p1TranscriptWordCount: document.getElementById('p1TranscriptWordCount'),
    p1TranscriptText: document.getElementById('p1TranscriptText'),
    p1UserAudioWrap: document.getElementById('p1UserAudioWrap'),
    p1UserAudioPlayer: document.getElementById('p1UserAudioPlayer'),
    btnToggleP1Sample: document.getElementById('btnToggleP1Sample'),
    p1SampleBox: document.getElementById('p1SampleBox'),
    btnP1ListenSample: document.getElementById('btnP1ListenSample'),
    p1SampleEn: document.getElementById('p1SampleEn'),
    p1SampleVi: document.getElementById('p1SampleVi'),
    p1VocabList: document.getElementById('p1VocabList'),
    p1TemplateList: document.getElementById('p1TemplateList'),
    btnP1PrevQ: document.getElementById('btnP1PrevQ'),
    btnP1NextQ: document.getElementById('btnP1NextQ'),
    p1QPillsContainer: document.getElementById('p1QPillsContainer'),
    // Part 2
    speakingP2TopicSelector: document.getElementById('speakingP2TopicSelector'),
    speakingP2TopicBadge: document.getElementById('speakingP2TopicBadge'),
    speakingP2TimeBadge: document.getElementById('speakingP2TimeBadge'),
    btnP2ListenTopic: document.getElementById('btnP2ListenTopic'),
    speakingP2TitleEn: document.getElementById('speakingP2TitleEn'),
    speakingP2TitleVi: document.getElementById('speakingP2TitleVi'),
    p2CuesGrid: document.getElementById('p2CuesGrid'),
    btnP2RecordToggle: document.getElementById('btnP2RecordToggle'),
    p2RecordBtnText: document.getElementById('p2RecordBtnText'),
    p2RecordTimer: document.getElementById('p2RecordTimer'),
    p2RecordTimerText: document.getElementById('p2RecordTimerText'),
    p2TranscriptWordCount: document.getElementById('p2TranscriptWordCount'),
    p2TranscriptText: document.getElementById('p2TranscriptText'),
    p2UserAudioWrap: document.getElementById('p2UserAudioWrap'),
    p2UserAudioPlayer: document.getElementById('p2UserAudioPlayer'),
    btnToggleP2Sample: document.getElementById('btnToggleP2Sample'),
    p2SampleBox: document.getElementById('p2SampleBox'),
    btnP2ListenFullSpeech: document.getElementById('btnP2ListenFullSpeech'),
    p2SpeechEn: document.getElementById('p2SpeechEn'),
    p2SpeechVi: document.getElementById('p2SpeechVi'),
    p2VocabList: document.getElementById('p2VocabList'),
    p2TransitionList: document.getElementById('p2TransitionList'),
    btnP2PrevTopic: document.getElementById('btnP2PrevTopic'),
    btnP2NextTopic: document.getElementById('btnP2NextTopic'),
    p2NavInfo: document.getElementById('p2NavInfo'),
    // Part 3 Exam
    speakingExamSetup: document.getElementById('speakingExamSetup'),
    examTypeP1: document.getElementById('examTypeP1'),
    examTypeP2: document.getElementById('examTypeP2'),
    examTypeFull: document.getElementById('examTypeFull'),
    btnStartSpeakingExam: document.getElementById('btnStartSpeakingExam'),
    speakingExamActive: document.getElementById('speakingExamActive'),
    examStepBadge: document.getElementById('examStepBadge'),
    examPhaseBadge: document.getElementById('examPhaseBadge'),
    btnQuitSpeakingExam: document.getElementById('btnQuitSpeakingExam'),
    examClockRing: document.getElementById('examClockRing'),
    examClockNumber: document.getElementById('examClockNumber'),
    examClockLabel: document.getElementById('examClockLabel'),
    examQText: document.getElementById('examQText'),
    examQCues: document.getElementById('examQCues'),
    examRecPulse: document.getElementById('examRecPulse'),
    examRecStatusText: document.getElementById('examRecStatusText'),
    examTranscriptPreview: document.getElementById('examTranscriptPreview'),
    btnSkipExamPrep: document.getElementById('btnSkipExamPrep'),
    btnNextExamItem: document.getElementById('btnNextExamItem'),
    speakingExamResult: document.getElementById('speakingExamResult'),
    examReviewList: document.getElementById('examReviewList'),
    btnRetakeSpeakingExam: document.getElementById('btnRetakeSpeakingExam'),
    btnBackToSpeakingPractice: document.getElementById('btnBackToSpeakingPractice'),

    // LAN Modal Elements
    btnLanModal: document.getElementById('btnLanModal'),
    lanModal: document.getElementById('lanModal'),
    modalQrImg: document.getElementById('modalQrImg'),
    modalLanUrlText: document.getElementById('modalLanUrlText'),
    btnModalCopyLanUrl: document.getElementById('btnModalCopyLanUrl'),
    btnModalOpenLanPage: document.getElementById('btnModalOpenLanPage'),
    btnModalCloseLan: document.getElementById('btnModalCloseLan'),
    heroLanUrl: document.getElementById('heroLanUrl'),
    btnHeroOpenLanModal: document.getElementById('btnHeroOpenLanModal'),

    // Speaking Study Elements
    btnSpeakingSubtabStudy: document.getElementById('btnSpeakingSubtabStudy'),
    viewSpeakingStudy: document.getElementById('viewSpeakingStudy'),
    speakingStudyFilterPills: document.getElementById('speakingStudyFilterPills'),
    speakingStudyCardsContainer: document.getElementById('speakingStudyCardsContainer'),
    speakingStudySearchInput: document.getElementById('speakingStudySearchInput'),
    btnClearStudySearch: document.getElementById('btnClearStudySearch'),
    speakingStudySpeedSelect: document.getElementById('speakingStudySpeedSelect'),
    btnToggleStudyViTranslation: document.getElementById('btnToggleStudyViTranslation')
  };

  // Shared audio instances
  let transAudio = new Audio();
  let editorAudio = new Audio();

  // =========================================================================
  // INITIALIZATION
  // =========================================================================
  function init() {
    applyAllOverrides();
    applyTheme(state.theme);
    bindEvents();
    renderHomeScreenSkill(state.currentSkill);
    initTranslationState();
    initWritingModule();
    initSpeakingModule();
    initLanAccess();
    showScreen('home');
  }

  // =========================================================================
  // THEME MANAGEMENT
  // =========================================================================
  function applyTheme(theme) {
    state.theme = theme;
    localStorage.setItem('toeic_theme', theme);
    if (theme === 'light') {
      document.body.classList.remove('theme-dark');
      document.body.classList.add('theme-light');
      el.themeIcon.textContent = '🌙';
    } else {
      document.body.classList.remove('theme-light');
      document.body.classList.add('theme-dark');
      el.themeIcon.textContent = '☀️';
    }
  }

  function toggleTheme() {
    applyTheme(state.theme === 'dark' ? 'light' : 'dark');
  }

  // =========================================================================
  // LAN / WI-FI ACCESS MANAGEMENT
  // =========================================================================
  async function initLanAccess() {
    try {
      const res = await fetch('/api/server_info');
      if (res.ok) {
        const data = await res.json();
        if (data && data.lan_url) {
          state.lanUrl = data.lan_url;
        }
      }
    } catch (e) {
      if (window.location.protocol === 'https:' || (window.location.hostname && window.location.hostname.includes('github.io'))) {
        state.lanUrl = window.location.href.split('#')[0];
      } else {
        const port = window.location.port ? `:${window.location.port}` : '';
        const host = (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1')
          ? window.location.hostname : '192.168.2.6';
        state.lanUrl = `${window.location.protocol}//${host}${port}/index.html`;
      }
    }

    if (el.heroLanUrl) el.heroLanUrl.textContent = state.lanUrl;
    if (el.modalLanUrlText) el.modalLanUrlText.textContent = state.lanUrl;
    if (el.modalQrImg) {
      const encoded = encodeURIComponent(state.lanUrl);
      el.modalQrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&margin=4&data=${encoded}`;
    }

    if (el.btnLanModal) {
      el.btnLanModal.addEventListener('click', () => {
        if (el.lanModal) el.lanModal.classList.add('active');
      });
    }

    if (el.btnHeroOpenLanModal) {
      el.btnHeroOpenLanModal.addEventListener('click', () => {
        if (el.lanModal) el.lanModal.classList.add('active');
      });
    }

    if (el.btnModalCloseLan) {
      el.btnModalCloseLan.addEventListener('click', () => {
        if (el.lanModal) el.lanModal.classList.remove('active');
      });
    }

    if (el.btnModalCopyLanUrl) {
      el.btnModalCopyLanUrl.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(state.lanUrl);
          showToast('📋 Đã sao chép liên kết mạng LAN!');
        } catch (e) {
          const inp = document.createElement('input');
          inp.value = state.lanUrl;
          document.body.appendChild(inp);
          inp.select();
          document.execCommand('copy');
          document.body.removeChild(inp);
          showToast('📋 Đã sao chép liên kết!');
        }
      });
    }
  }

  // =========================================================================
  // EVENT BINDINGS
  // =========================================================================
  function bindEvents() {
    // Theme toggle
    el.btnThemeToggle.addEventListener('click', toggleTheme);

    // Top Navigation Tabs
    el.tabNavListening.addEventListener('click', () => {
      setSkill('listening');
      showScreen('home');
    });

    el.tabNavReading.addEventListener('click', () => {
      setSkill('reading');
      showScreen('home');
    });

    el.tabNavTranslation.addEventListener('click', () => {
      stopAudio();
      stopTransAudio();
      openTranslationMode();
    });

    el.tabNavWriting.addEventListener('click', () => {
      stopAudio();
      stopTransAudio();
      stopEditorAudio();
      openWritingMode();
    });

    if (el.tabNavSpeaking) {
      el.tabNavSpeaking.addEventListener('click', () => {
        stopAudio();
        stopTransAudio();
        stopEditorAudio();
        stopAllSpeakingAudio();
        openSpeakingMode();
      });
    }

    if (el.modeCardSpeaking) {
      el.modeCardSpeaking.addEventListener('click', () => {
        stopAudio();
        stopTransAudio();
        stopEditorAudio();
        stopAllSpeakingAudio();
        openSpeakingMode();
      });
    }

    el.tabNavEditor.addEventListener('click', () => {
      stopAudio();
      stopTransAudio();
      stopEditorAudio();
      openEditorMode();
    });

    // Home Skill Toggles
    el.skillToggleListening.addEventListener('click', () => setSkill('listening'));
    el.skillToggleReading.addEventListener('click', () => setSkill('reading'));

    // Reading Shuffle Options Toggle
    if (el.chkReadingShuffle) {
      el.chkReadingShuffle.checked = state.readingShuffle;
      el.chkReadingShuffle.addEventListener('change', (e) => {
        state.readingShuffle = e.target.checked;
        localStorage.setItem('toeic_reading_shuffle', state.readingShuffle ? 'true' : 'false');
        showToast(state.readingShuffle 
          ? '🔀 Đã BẬT chế độ đảo đáp án khi kiểm tra Reading!' 
          : '⏹️ Đã TẮT chế độ đảo đáp án (sử dụng thứ tự gốc)');
      });
    }

    // Listening Hide Text Toggle (Only show A B C D)
    if (el.chkListeningHide) {
      el.chkListeningHide.checked = state.listeningHideText;
      el.chkListeningHide.addEventListener('change', (e) => {
        state.listeningHideText = e.target.checked;
        localStorage.setItem('toeic_listening_hide_text', state.listeningHideText ? 'true' : 'false');
        if (el.chkPreTestListeningHide) el.chkPreTestListeningHide.checked = state.listeningHideText;
        showToast(state.listeningHideText 
          ? '🙈 Đã BẬT ẩn chữ đáp án (chỉ để lại A, B, C, D) cho đề thi Listening!' 
          : '👁️ Đã TẮT ẩn chữ (hiển thị đầy đủ chữ các đáp án)');
      });
    }

    // Home Mode Selection
    if (el.modeCardStudy) el.modeCardStudy.addEventListener('click', () => setMode('study'));
    el.modeCardExam.addEventListener('click', () => setMode('exam'));
    el.modeCardPractice.addEventListener('click', () => setMode('practice'));
    el.modeCardTranslation.addEventListener('click', () => openTranslationMode());
    el.modeCardWriting.addEventListener('click', () => openWritingMode());
    el.modeCardEditor.addEventListener('click', () => openEditorMode());

    // Exit Test / Change Test
    el.btnExitTest.addEventListener('click', () => {
      if (state.activeScreen === 'writing' || state.activeScreen === 'translation' || state.activeScreen === 'editor' || confirm('Bạn có chắc muốn thoát bài thi hiện tại và quay về màn hình chính?')) {
        stopTimer();
        stopAudio();
        stopTransAudio();
        stopEditorAudio();
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        showScreen('home');
      }
    });

    // Question Editor Toolbar Events
    el.editorSearchInput.addEventListener('input', debounce((e) => {
      state.editorSearchQuery = e.target.value.trim().toLowerCase();
      state.editorVisibleLimit = 20;
      renderEditorQuestions();
    }, 250));

    el.btnClearEditorSearch.addEventListener('click', () => {
      el.editorSearchInput.value = '';
      state.editorSearchQuery = '';
      state.editorVisibleLimit = 20;
      renderEditorQuestions();
    });

    el.editorFilterSkill.addEventListener('change', (e) => {
      state.editorFilterSkill = e.target.value;
      state.editorVisibleLimit = 20;
      renderEditorQuestions();
    });

    el.editorFilterTest.addEventListener('change', (e) => {
      state.editorFilterTest = e.target.value;
      state.editorVisibleLimit = 20;
      renderEditorQuestions();
    });

    el.editorFilterPart.addEventListener('change', (e) => {
      state.editorFilterPart = e.target.value;
      state.editorVisibleLimit = 20;
      renderEditorQuestions();
    });

    el.editorFilterEdited.addEventListener('change', (e) => {
      state.editorFilterEdited = e.target.value;
      state.editorVisibleLimit = 20;
      renderEditorQuestions();
    });

    el.btnEditorLoadMore.addEventListener('click', () => {
      state.editorVisibleLimit += 20;
      renderEditorQuestions(true);
    });

    el.btnExportCustomData.addEventListener('click', exportCustomData);
    el.btnResetAllOverrides.addEventListener('click', resetAllOverrides);

    // Question Navigation
    el.btnPrevQuestion.addEventListener('click', goToPrevQuestion);
    el.btnNextQuestion.addEventListener('click', goToNextQuestion);
    el.btnFlagQuestion.addEventListener('click', toggleFlagCurrentQuestion);

    // Audio Player Events
    el.btnAudioPlayPause.addEventListener('click', toggleAudioPlay);
    el.btnAudioRewind.addEventListener('click', () => seekAudio(-5));
    el.btnAudioForward.addEventListener('click', () => seekAudio(5));
    el.audioSpeedSelect.addEventListener('change', (e) => {
      el.audioPlayer.playbackRate = parseFloat(e.target.value);
    });

    el.audioPlayer.addEventListener('timeupdate', updateAudioProgress);
    el.audioPlayer.addEventListener('loadedmetadata', () => {
      el.audioTotalDuration.textContent = formatTime(el.audioPlayer.duration || 0);
    });
    el.audioPlayer.addEventListener('ended', () => {
      el.playPauseIcon.textContent = '▶️';
      el.audioWaveAnim.classList.remove('playing');
    });
    el.audioPlayer.addEventListener('play', () => {
      el.playPauseIcon.textContent = '⏸️';
      el.audioWaveAnim.classList.add('playing');
    });
    el.audioPlayer.addEventListener('pause', () => {
      el.playPauseIcon.textContent = '▶️';
      el.audioWaveAnim.classList.remove('playing');
    });

    el.audioSeekBar.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      if (el.audioPlayer.duration) {
        el.audioPlayer.currentTime = (val / 100) * el.audioPlayer.duration;
      }
    });

    // Submit Exam Buttons
    el.btnTopSubmit.addEventListener('click', promptSubmitExam);
    el.btnSubmitExam.addEventListener('click', promptSubmitExam);
    el.btnCancelSubmit.addEventListener('click', () => el.confirmModal.classList.remove('active'));
    el.btnConfirmSubmit.addEventListener('click', submitExam);

    // Score Review Filters
    document.querySelectorAll('.review-filter-buttons .filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.review-filter-buttons .filter-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        state.filterReview = e.currentTarget.dataset.filter;
        renderReviewList();
      });
    });

    // Retake / Choose Another Test
    el.btnRetakeTest.addEventListener('click', () => {
      const isPart = (typeof state.testId === 'string' && state.testId.startsWith('part_'));
      const id = isPart ? parseInt(state.testId.replace('part_', ''), 10) : state.testId;
      const type = isPart ? 'part' : 'test';
      promptPreTestStart(type, id, state.currentSkill);
    });
    el.btnChooseAnotherTest.addEventListener('click', () => showScreen('home'));

    // Pre-test Setup Modal Event Listeners
    if (el.preTestModeStudy) {
      el.preTestModeStudy.addEventListener('click', () => {
        setMode('study');
      });
    }
    if (el.preTestModeExam) {
      el.preTestModeExam.addEventListener('click', () => {
        setMode('exam');
      });
    }
    if (el.preTestModePractice) {
      el.preTestModePractice.addEventListener('click', () => {
        setMode('practice');
      });
    }

    if (el.btnStudyToExam) {
      el.btnStudyToExam.addEventListener('click', switchToExamFromStudy);
    }

    if (el.chkPreTestShuffle) {
      el.chkPreTestShuffle.addEventListener('change', (e) => {
        state.readingShuffle = e.target.checked;
        localStorage.setItem('toeic_reading_shuffle', state.readingShuffle ? 'true' : 'false');
        if (el.chkReadingShuffle) el.chkReadingShuffle.checked = state.readingShuffle;
        showToast(state.readingShuffle 
          ? '🔀 Đã BẬT đảo thứ tự đáp án (A, B, C, D)!' 
          : '⏹️ Đã TẮT đảo đáp án (Sử dụng thứ tự gốc)!');
      });
    }

    if (el.chkPreTestListeningHide) {
      el.chkPreTestListeningHide.addEventListener('change', (e) => {
        state.listeningHideText = e.target.checked;
        localStorage.setItem('toeic_listening_hide_text', state.listeningHideText ? 'true' : 'false');
        if (el.chkListeningHide) el.chkListeningHide.checked = state.listeningHideText;
        showToast(state.listeningHideText 
          ? '🙈 Đã BẬT ẩn chữ đáp án (chỉ để lại A, B, C, D)!' 
          : '👁️ Đã TẮT ẩn chữ (hiển thị đầy đủ chữ các đáp án)!');
      });
    }

    if (el.btnCancelPreTest) {
      el.btnCancelPreTest.addEventListener('click', () => {
        el.preTestModal.classList.remove('active');
      });
    }

    if (el.btnConfirmStartTest) {
      el.btnConfirmStartTest.addEventListener('click', () => {
        el.preTestModal.classList.remove('active');
        executePreTestStart();
      });
    }

    if (el.btnToggleShuffleInExam) {
      el.btnToggleShuffleInExam.addEventListener('click', toggleShuffleInExam);
    }

    if (el.btnToggleListeningHideInExam) {
      el.btnToggleListeningHideInExam.addEventListener('click', toggleListeningHideInExam);
    }

    if (el.btnPeekListening) {
      el.btnPeekListening.addEventListener('click', togglePeekListeningCurrentQuestion);
    }

    // =======================================================================
    // TRANSLATION MODE EVENT LISTENERS
    // =======================================================================
    el.btnDirEnVi.addEventListener('click', () => setTransDirection('en-vi'));
    el.btnDirViEn.addEventListener('click', () => setTransDirection('vi-en'));

    el.transSelectSkill.addEventListener('change', (e) => {
      state.transSkill = e.target.value;
      filterTranslationData();
    });

    el.transSelectTest.addEventListener('change', (e) => {
      state.transTest = e.target.value;
      filterTranslationData();
    });

    el.transSelectPart.addEventListener('change', (e) => {
      state.transPart = e.target.value;
      filterTranslationData();
    });

    el.btnTransAudioPlay.addEventListener('click', toggleTransAudio);
    el.transAudioSpeed.addEventListener('change', (e) => {
      transAudio.playbackRate = parseFloat(e.target.value);
    });

    el.btnToggleHint.addEventListener('click', toggleTransHint);
    el.btnRevealTranslation.addEventListener('click', revealTranslation);

    // Self rating buttons
    document.querySelectorAll('.rating-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const rating = e.currentTarget.dataset.rating;
        rateCurrentTranslation(rating);
      });
    });

    el.btnTransPrev.addEventListener('click', () => {
      if (state.transIndex > 0) loadTranslationCard(state.transIndex - 1);
    });

    el.btnTransNext.addEventListener('click', () => {
      if (state.transIndex < state.transQuestions.length - 1) loadTranslationCard(state.transIndex + 1);
    });

    el.btnResetTransProgress.addEventListener('click', () => {
      if (confirm('Bạn có chắc muốn đặt lại toàn bộ tiến độ đánh giá luyện dịch câu?')) {
        state.transRatings = {};
        localStorage.removeItem('toeic_trans_ratings');
        loadTranslationCard(state.transIndex);
      }
    });

    // Writing Mode Subtab Switchers
    el.btnWritingSubtabParagraph.addEventListener('click', () => switchWritingSubtab('paragraph'));
    el.btnWritingSubtabQA.addEventListener('click', () => switchWritingSubtab('qa'));

    // Writing Structure Collapse Toggle
    el.btnToggleStructure.addEventListener('click', toggleWritingStructure);

    // Paragraph Writing Events
    el.paragraphTextarea.addEventListener('input', updateParagraphWordCount);
    el.btnSpeakUserParagraph.addEventListener('click', () => speakText(el.paragraphTextarea.value));
    el.btnSpeakSampleParagraph.addEventListener('click', () => {
      const topic = getWritingParagraphs()[state.writingParagraphIndex];
      if (topic) speakText(topic.sampleEn);
    });
    el.btnSpeakSampleParaPrompt.addEventListener('click', () => {
      const topic = getWritingParagraphs()[state.writingParagraphIndex];
      if (topic) speakText(topic.title);
    });
    el.btnRevealParagraphSample.addEventListener('click', revealParagraphSample);

    // QA Writing Events
    el.qaAnswerTextarea.addEventListener('input', updateQAWordCount);
    el.btnSpeakUserQA.addEventListener('click', () => speakText(el.qaAnswerTextarea.value));
    el.btnSpeakQAQuestion.addEventListener('click', () => {
      const q = getAllQAQuestions()[state.writingQAIndex];
      if (q) speakText(q.q);
    });
    el.btnSpeakQASample.addEventListener('click', () => {
      const q = getAllQAQuestions()[state.writingQAIndex];
      if (q) speakText(q.a);
    });
    el.btnRevealQASample.addEventListener('click', revealQASample);
    el.btnQAPrev.addEventListener('click', () => {
      if (state.writingQAIndex > 0) loadQAQuestion(state.writingQAIndex - 1);
    });
    el.btnQANext.addEventListener('click', () => {
      const qList = getAllQAQuestions();
      if (state.writingQAIndex < qList.length - 1) loadQAQuestion(state.writingQAIndex + 1);
    });

    // Clear and Reset Drafts
    el.btnWritingClearDraft.addEventListener('click', clearCurrentWritingDraft);
    el.btnResetAllWritingDrafts.addEventListener('click', resetAllWritingDrafts);

    // Keyboard Shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
  }

  // =========================================================================
  // SKILL SWITCHER (LISTENING vs READING)
  // =========================================================================
  function setSkill(skill) {
    state.currentSkill = skill;
    stopAudio();
    stopTransAudio();

    if (skill === 'listening') {
      el.tabNavListening.classList.add('active');
      el.tabNavReading.classList.remove('active');
      el.tabNavTranslation.classList.remove('active');
      el.tabNavWriting.classList.remove('active');
      el.skillToggleListening.classList.add('active');
      el.skillToggleReading.classList.remove('active');
    } else {
      el.tabNavReading.classList.add('active');
      el.tabNavListening.classList.remove('active');
      el.tabNavTranslation.classList.remove('active');
      el.tabNavWriting.classList.remove('active');
      el.skillToggleReading.classList.add('active');
      el.skillToggleListening.classList.remove('active');
    }

    renderHomeScreenSkill(skill);
  }

  function renderHomeScreenSkill(skill) {
    if (skill === 'listening') {
      if (el.readingShuffleToggleWrap) el.readingShuffleToggleWrap.style.display = 'none';
      if (el.listeningHideToggleWrap) el.listeningHideToggleWrap.style.display = 'flex';
      el.testSectionTitle.textContent = '2. Chọn bộ đề thi TOEIC Listening (Test 1 - 4):';
      el.testsGridContainer.innerHTML = `
        ${[1, 2, 3, 4].map(t => `
          <div class="test-card" data-test="${t}">
            <div class="test-card-top">
              <span class="test-badge">LISTENING FULL</span>
              <span class="test-duration">45 phút</span>
            </div>
            <h3>TOEIC Listening Test ${t}</h3>
            <p>70 câu chuẩn TOEIC (Part 1: 6 tranh, Part 2: 25 câu hỏi đáp, Part 3: 39 câu hội thoại).</p>
            <div class="test-card-stats">
              <span>🖼️ 6 Ảnh</span>
              <span>🔊 44 Audio</span>
              <span>📝 70 Câu</span>
            </div>
            <div class="test-card-actions">
              <button class="btn btn-primary btn-start-test" data-test="${t}">⏱️ Thi Thử</button>
              <button class="btn btn-start-study btn-start-study-test" data-test="${t}">📚 Học Trước</button>
            </div>
          </div>
        `).join('')}
      `;

      el.partPracticeTitle.textContent = '🎯 Cày riêng từng Part kỹ năng Nghe (Listening)?';
      el.partPracticeSub.textContent = 'Gom 4 bài test để luyện chuyên sâu 1 phần cụ thể.';
      el.partButtonsGroup.innerHTML = `
        <button class="btn btn-outline btn-start-part" data-part="1">🖼️ Cày 24 câu Part 1 (Tranh)</button>
        <button class="btn btn-outline btn-start-part" data-part="2">❓ Cày 100 câu Part 2 (Hỏi đáp)</button>
        <button class="btn btn-outline btn-start-part" data-part="3">👥 Cày 156 câu Part 3 (Hội thoại)</button>
      `;
    } else {
      if (el.readingShuffleToggleWrap) el.readingShuffleToggleWrap.style.display = 'flex';
      if (el.listeningHideToggleWrap) el.listeningHideToggleWrap.style.display = 'none';
      el.testSectionTitle.textContent = '2. Chọn bộ đề thi TOEIC Reading B1 (Test 1 - 4):';
      el.testsGridContainer.innerHTML = `
        ${[1, 2, 3, 4].map(t => `
          <div class="test-card" data-test="${t}">
            <div class="test-card-top">
              <span class="test-badge" style="background:rgba(16, 185, 129, 0.15); color:#10b981;">READING B1</span>
              <span class="test-duration">45 phút</span>
            </div>
            <h3>TOEIC Reading Test ${t}</h3>
            <p>50 câu đọc hiểu B1 (Part 1: 30 câu điền câu, Part 2: 16 câu điền đoạn văn, Part 3: 4 câu đọc hiểu).</p>
            <div class="test-card-stats">
              <span>✏️ 30 Điền câu</span>
              <span>📄 16 Điền đoạn</span>
              <span>📝 50 Câu</span>
            </div>
            <div class="test-card-actions">
              <button class="btn btn-primary btn-start-test" data-test="${t}" style="background:#10b981;">⏱️ Thi Thử</button>
              <button class="btn btn-start-study btn-start-study-test" data-test="${t}">📚 Học Trước</button>
            </div>
          </div>
        `).join('')}
      `;

      el.partPracticeTitle.textContent = '🎯 Cày riêng từng Part kỹ năng Đọc (Reading B1)?';
      el.partPracticeSub.textContent = 'Luyện chuyên sâu ngữ pháp, từ vựng và kỹ năng đọc hiểu văn bản.';
      el.partButtonsGroup.innerHTML = `
        <button class="btn btn-outline btn-start-part" data-part="1">✏️ Cày 120 câu Part 1 (Điền câu)</button>
        <button class="btn btn-outline btn-start-part" data-part="2">📄 Cày 64 câu Part 2 (Điền đoạn)</button>
        <button class="btn btn-outline btn-start-part" data-part="3">📰 Cày 16 câu Part 3 (Đọc hiểu)</button>
      `;
    }

    // Rebind dynamic test start buttons
    el.testsGridContainer.querySelectorAll('.btn-start-test').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const testNum = parseInt(e.currentTarget.dataset.test, 10);
        if (state.mode === 'study') setMode('exam');
        promptPreTestStart('test', testNum, skill);
      });
    });

    el.testsGridContainer.querySelectorAll('.btn-start-study-test').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const testNum = parseInt(e.currentTarget.dataset.test, 10);
        setMode('study');
        promptPreTestStart('test', testNum, skill);
      });
    });

    el.partButtonsGroup.querySelectorAll('.btn-start-part').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const partNum = parseInt(e.currentTarget.dataset.part, 10);
        promptPreTestStart('part', partNum, skill);
      });
    });
  }

  // =========================================================================
  // SCREEN SWITCHER
  // =========================================================================
  function showScreen(screenName) {
    state.activeScreen = screenName;
    el.screenHome.classList.remove('active');
    el.screenExam.classList.remove('active');
    el.screenScore.classList.remove('active');
    el.screenTranslation.classList.remove('active');
    el.screenWriting.classList.remove('active');
    if (el.screenSpeaking) el.screenSpeaking.classList.remove('active');
    if (el.screenEditor) el.screenEditor.classList.remove('active');

    if (screenName === 'home') {
      el.screenHome.classList.add('active');
      if (state.currentSkill === 'listening') {
        el.tabNavListening.classList.add('active');
        el.tabNavReading.classList.remove('active');
      } else {
        el.tabNavReading.classList.add('active');
        el.tabNavListening.classList.remove('active');
      }
      el.tabNavTranslation.classList.remove('active');
      el.tabNavWriting.classList.remove('active');
      if (el.tabNavSpeaking) el.tabNavSpeaking.classList.remove('active');
      if (el.tabNavEditor) el.tabNavEditor.classList.remove('active');
      el.navCenterInfo.style.display = 'none';
      el.btnTopSubmit.style.display = 'none';
      el.btnExitTest.style.display = 'none';
    } else if (screenName === 'exam') {
      el.screenExam.classList.add('active');
      el.navCenterInfo.style.display = 'flex';
      el.btnExitTest.style.display = 'flex';
      if (state.mode === 'study') {
        el.btnTopSubmit.style.display = 'inline-flex';
        el.btnTopSubmit.innerHTML = '<span>Thi Thử Ngay</span> 🚀';
        el.btnTopSubmit.classList.add('btn-mode-study-submit');
      } else if (state.mode === 'exam') {
        el.btnTopSubmit.style.display = 'inline-flex';
        el.btnTopSubmit.innerHTML = '<span>Nộp Bài</span> 🚀';
        el.btnTopSubmit.classList.remove('btn-mode-study-submit');
      } else {
        el.btnTopSubmit.style.display = 'none';
        el.btnTopSubmit.classList.remove('btn-mode-study-submit');
      }
    } else if (screenName === 'score') {
      el.screenScore.classList.add('active');
      el.navCenterInfo.style.display = 'none';
      el.btnTopSubmit.style.display = 'none';
      el.btnExitTest.style.display = 'flex';
    } else if (screenName === 'translation') {
      el.screenTranslation.classList.add('active');
      el.tabNavTranslation.classList.add('active');
      el.tabNavListening.classList.remove('active');
      el.tabNavReading.classList.remove('active');
      el.tabNavWriting.classList.remove('active');
      if (el.tabNavSpeaking) el.tabNavSpeaking.classList.remove('active');
      if (el.tabNavEditor) el.tabNavEditor.classList.remove('active');
      el.navCenterInfo.style.display = 'none';
      el.btnTopSubmit.style.display = 'none';
      el.btnExitTest.style.display = 'flex';
    } else if (screenName === 'writing') {
      el.screenWriting.classList.add('active');
      el.tabNavWriting.classList.add('active');
      el.tabNavListening.classList.remove('active');
      el.tabNavReading.classList.remove('active');
      el.tabNavTranslation.classList.remove('active');
      if (el.tabNavSpeaking) el.tabNavSpeaking.classList.remove('active');
      if (el.tabNavEditor) el.tabNavEditor.classList.remove('active');
      el.navCenterInfo.style.display = 'none';
      el.btnTopSubmit.style.display = 'none';
      el.btnExitTest.style.display = 'flex';
    } else if (screenName === 'speaking') {
      if (el.screenSpeaking) el.screenSpeaking.classList.add('active');
      if (el.tabNavSpeaking) el.tabNavSpeaking.classList.add('active');
      el.tabNavListening.classList.remove('active');
      el.tabNavReading.classList.remove('active');
      el.tabNavTranslation.classList.remove('active');
      el.tabNavWriting.classList.remove('active');
      if (el.tabNavEditor) el.tabNavEditor.classList.remove('active');
      el.navCenterInfo.style.display = 'none';
      el.btnTopSubmit.style.display = 'none';
      el.btnExitTest.style.display = 'flex';
    } else if (screenName === 'editor') {
      if (el.screenEditor) el.screenEditor.classList.add('active');
      if (el.tabNavEditor) el.tabNavEditor.classList.add('active');
      el.tabNavListening.classList.remove('active');
      el.tabNavReading.classList.remove('active');
      el.tabNavTranslation.classList.remove('active');
      el.tabNavWriting.classList.remove('active');
      if (el.tabNavSpeaking) el.tabNavSpeaking.classList.remove('active');
      el.navCenterInfo.style.display = 'none';
      el.btnTopSubmit.style.display = 'none';
      el.btnExitTest.style.display = 'flex';
    }
  }

  function setMode(mode) {
    state.mode = mode;
    if (el.modeCardExam) el.modeCardExam.classList.toggle('active', mode === 'exam');
    if (el.modeCardPractice) el.modeCardPractice.classList.toggle('active', mode === 'practice');
    if (el.modeCardStudy) el.modeCardStudy.classList.toggle('active', mode === 'study');

    if (el.preTestModeExam) el.preTestModeExam.classList.toggle('active', mode === 'exam');
    if (el.preTestModePractice) el.preTestModePractice.classList.toggle('active', mode === 'practice');
    if (el.preTestModeStudy) el.preTestModeStudy.classList.toggle('active', mode === 'study');
  }

  // =========================================================================
  // TEST INITIALIZATION & SHUFFLE OPTIONS LOGIC
  // =========================================================================
  function prepareTestQuestions(questions, isReading) {
    if (!isReading || !state.readingShuffle) {
      return questions.map(q => ({
        ...q,
        options: q.options ? q.options.map(o => ({ ...o })) : []
      }));
    }

    const letters = ['A', 'B', 'C', 'D'];

    return questions.map(q => {
      if (!q.options || q.options.length <= 1) {
        return {
          ...q,
          options: q.options ? q.options.map(o => ({ ...o })) : []
        };
      }

      const origCorrectKey = q.correctAnswer;
      const origCorrectOpt = q.options.find(o => o.key === origCorrectKey);
      const origCorrectText = origCorrectOpt ? origCorrectOpt.text : null;

      // Deep clone options
      const clonedOptions = q.options.map(o => ({ ...o }));

      // Fisher-Yates shuffle
      for (let i = clonedOptions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [clonedOptions[i], clonedOptions[j]] = [clonedOptions[j], clonedOptions[i]];
      }

      let newCorrectKey = origCorrectKey;
      const remappedOptions = clonedOptions.map((opt, idx) => {
        const key = letters[idx] || opt.key;
        if (opt.key === origCorrectKey || (origCorrectText && opt.text === origCorrectText)) {
          newCorrectKey = key;
        }
        return {
          key: key,
          text: opt.text
        };
      });

      // Update explanation if correct key changed
      let explanation = q.explanation || '';
      if (newCorrectKey !== origCorrectKey) {
        const noteBadge = `<div class="shuffle-note-badge" style="margin-bottom:8px; padding:6px 10px; background:rgba(16, 185, 129, 0.12); border-left:3px solid #10b981; font-size:12.5px; border-radius:3px; color:var(--text-main);">🔀 <i>Thứ tự đáp án đã được đảo ngẫu nhiên. Đáp án đúng của câu này là <strong>(${newCorrectKey})</strong> (vị trí ban đầu: ${origCorrectKey}).</i></div>`;
        const replacedExp = explanation.replace(
          new RegExp(`(Đáp án đúng:?\\s*<b>?\\(?)${origCorrectKey}(\\)?</b>?)`, 'i'),
          `$1${newCorrectKey}$2`
        );
        explanation = noteBadge + replacedExp;
      }

      return {
        ...q,
        options: remappedOptions,
        correctAnswer: newCorrectKey,
        originalCorrectAnswer: origCorrectKey,
        explanation: explanation,
        isOptionsShuffled: true
      };
    });
  }

  function startTest(testNum) {
    const isReading = (state.currentSkill === 'reading');
    const rawData = isReading ? (window.TOEIC_READING_DATA || []) : (window.TOEIC_DATA || []);
    const filtered = rawData.filter(q => q.test === testNum);

    if (!filtered.length) {
      alert(`Không tìm thấy dữ liệu cho ${state.currentSkill} Test ${testNum}.`);
      return;
    }

    state.testId = testNum;
    state.questions = prepareTestQuestions(filtered, isReading);
    resetTestState();

    const skillLabel = isReading ? 'Reading B1' : 'Listening';
    el.currentTestDisplay.textContent = `${skillLabel} Test ${testNum}`;
    
    let modeLabel = 'Thi Thử (45m)';
    if (state.mode === 'practice') modeLabel = 'Luyện Tập';
    if (state.mode === 'study') modeLabel = '📚 Học Trước Khi Thi';
    el.currentModeDisplay.textContent = modeLabel;

    setupPalette();
    showScreen('exam');
    loadQuestion(0);

    if (state.mode === 'exam') {
      startTimer(45 * 60);
      if (el.studyModeBanner) el.studyModeBanner.style.display = 'none';
      if (el.btnSubmitExam) el.btnSubmitExam.textContent = 'Nộp Bài Thi';
    } else if (state.mode === 'study') {
      stopTimer();
      el.timerCountdown.textContent = '📚 Chế Độ Học';
      if (el.studyModeBanner) el.studyModeBanner.style.display = 'flex';
      if (el.btnSubmitExam) el.btnSubmitExam.textContent = '🚀 Đã Học Xong - Thi Thử Ngay';
    } else {
      stopTimer();
      el.timerCountdown.textContent = 'Luyện tập';
      if (el.studyModeBanner) el.studyModeBanner.style.display = 'none';
      if (el.btnSubmitExam) el.btnSubmitExam.textContent = 'Nộp Bài / Xem Kết Quả';
    }
  }

  function startPartTest(partNum) {
    const isReading = (state.currentSkill === 'reading');
    const rawData = isReading ? (window.TOEIC_READING_DATA || []) : (window.TOEIC_DATA || []);
    const filtered = rawData.filter(q => q.part === partNum);

    if (!filtered.length) {
      alert(`Không tìm thấy dữ liệu cho Part ${partNum}.`);
      return;
    }

    state.testId = `part_${partNum}`;
    state.questions = prepareTestQuestions(filtered, isReading);
    resetTestState();

    const skillLabel = isReading ? 'Reading B1' : 'Listening';
    el.currentTestDisplay.textContent = `${skillLabel} Part ${partNum}`;

    let modeLabel = 'Thi Thử';
    if (state.mode === 'practice') modeLabel = 'Luyện Tập';
    if (state.mode === 'study') modeLabel = '📚 Học Trước Khi Thi';
    el.currentModeDisplay.textContent = modeLabel;

    setupPalette();
    showScreen('exam');
    loadQuestion(0);

    if (state.mode === 'exam') {
      const minutes = (filtered.length <= 25) ? 20 : (filtered.length <= 70 ? 45 : 60);
      startTimer(minutes * 60);
      if (el.studyModeBanner) el.studyModeBanner.style.display = 'none';
      if (el.btnSubmitExam) el.btnSubmitExam.textContent = 'Nộp Bài Thi';
    } else if (state.mode === 'study') {
      stopTimer();
      el.timerCountdown.textContent = '📚 Chế Độ Học';
      if (el.studyModeBanner) el.studyModeBanner.style.display = 'flex';
      if (el.btnSubmitExam) el.btnSubmitExam.textContent = '🚀 Đã Học Xong - Thi Thử Ngay';
    } else {
      stopTimer();
      el.timerCountdown.textContent = 'Luyện tập';
      if (el.studyModeBanner) el.studyModeBanner.style.display = 'none';
      if (el.btnSubmitExam) el.btnSubmitExam.textContent = 'Nộp Bài / Xem Kết Quả';
    }
  }

  function resetTestState() {
    state.currentIndex = 0;
    state.userAnswers = {};
    state.flaggedQuestions = {};
    state.timeSpentSeconds = 0;
    state.listeningPeekQuestionId = null;
    stopAudio();
  }

  // =========================================================================
  // PRE-TEST SETUP CONTROLLER
  // =========================================================================
  function promptPreTestStart(type, id, skill) {
    state.preTestTarget = { type, id, skill };

    const isReading = (skill === 'reading');
    const skillName = isReading ? 'TOEIC Reading B1' : 'TOEIC Listening';
    const icon = isReading ? '📖' : '🎧';

    let title = '';
    let desc = '';

    if (type === 'test') {
      title = `${skillName} Test ${id}`;
      desc = isReading 
        ? `Bộ đề thi 50 câu đọc hiểu chuẩn B1 (Part 1: 30 câu, Part 2: 16 câu, Part 3: 4 câu). Thời gian chuẩn: 45 phút.`
        : `Bộ đề thi 70 câu chuẩn TOEIC (Part 1: 6 tranh, Part 2: 25 câu, Part 3: 39 câu). Thời gian chuẩn: 45 phút.`;
    } else {
      const partNum = id;
      title = `${skillName} - Part ${partNum}`;
      desc = isReading
        ? `Luyện chuyên sâu Part ${partNum} Reading (${partNum === 1 ? '120 câu Điền vào câu' : (partNum === 2 ? '64 câu Điền đoạn văn' : '16 câu Đọc hiểu')}).`
        : `Luyện chuyên sâu Part ${partNum} Listening (${partNum === 1 ? '24 câu Tranh' : (partNum === 2 ? '100 câu Hỏi đáp' : '156 câu Hội thoại')}).`;
    }

    if (el.preTestIcon) el.preTestIcon.textContent = icon;
    if (el.preTestTitle) el.preTestTitle.textContent = title;
    if (el.preTestDesc) el.preTestDesc.textContent = desc;

    // Sync mode buttons
    if (el.preTestModeStudy) el.preTestModeStudy.classList.toggle('active', state.mode === 'study');
    if (el.preTestModeExam) el.preTestModeExam.classList.toggle('active', state.mode === 'exam');
    if (el.preTestModePractice) el.preTestModePractice.classList.toggle('active', state.mode === 'practice');

    // Sync shuffle checkbox
    if (el.chkPreTestShuffle) {
      el.chkPreTestShuffle.checked = state.readingShuffle;
    }

    // Only show shuffle option row for Reading
    if (el.preTestShuffleRow) {
      el.preTestShuffleRow.style.display = isReading ? 'block' : 'none';
    }

    // Sync listening hide checkbox & visibility (Only for Listening)
    if (el.chkPreTestListeningHide) {
      el.chkPreTestListeningHide.checked = state.listeningHideText;
    }
    if (el.preTestListeningHideRow) {
      el.preTestListeningHideRow.style.display = (!isReading) ? 'block' : 'none';
    }

    if (el.preTestModal) {
      el.preTestModal.classList.add('active');
    }
  }

  function executePreTestStart() {
    if (!state.preTestTarget) return;
    const { type, id } = state.preTestTarget;
    if (type === 'test') {
      startTest(id);
    } else {
      startPartTest(id);
    }
  }

  function toggleShuffleInExam() {
    if (state.currentSkill !== 'reading') return;
    state.readingShuffle = !state.readingShuffle;
    localStorage.setItem('toeic_reading_shuffle', state.readingShuffle ? 'true' : 'false');
    if (el.chkReadingShuffle) el.chkReadingShuffle.checked = state.readingShuffle;
    if (el.chkPreTestShuffle) el.chkPreTestShuffle.checked = state.readingShuffle;

    // Re-prepare questions with new shuffle setting
    const isReading = true;
    const rawData = window.TOEIC_READING_DATA || [];
    let currentFiltered = [];
    if (typeof state.testId === 'number') {
      currentFiltered = rawData.filter(q => q.test === state.testId);
    } else {
      const pNum = parseInt(state.testId.replace('part_', ''), 10);
      currentFiltered = rawData.filter(q => q.part === pNum);
    }

    const savedIndex = state.currentIndex;
    state.questions = prepareTestQuestions(currentFiltered, isReading);
    loadQuestion(savedIndex);

    updateShuffleInExamButton();

    showToast(state.readingShuffle 
      ? '🔀 Đã BẬT đảo thứ tự đáp án (A, B, C, D)!' 
      : '⏹️ Đã TẮT đảo đáp án (Sử dụng thứ tự gốc)!');
  }

  function updateShuffleInExamButton() {
    if (!el.btnToggleShuffleInExam) return;
    if (state.currentSkill === 'reading') {
      el.btnToggleShuffleInExam.style.display = 'inline-flex';
      if (el.shuffleBtnText) {
        el.shuffleBtnText.textContent = state.readingShuffle ? 'Đang đảo đáp án' : 'Đảo đáp án: Tắt';
      }
      if (state.readingShuffle) {
        el.btnToggleShuffleInExam.classList.add('active');
      } else {
        el.btnToggleShuffleInExam.classList.remove('active');
      }
    } else {
      el.btnToggleShuffleInExam.style.display = 'none';
    }
  }

  function toggleListeningHideInExam() {
    if (state.currentSkill !== 'listening') return;
    state.listeningHideText = !state.listeningHideText;
    localStorage.setItem('toeic_listening_hide_text', state.listeningHideText ? 'true' : 'false');
    if (el.chkListeningHide) el.chkListeningHide.checked = state.listeningHideText;
    if (el.chkPreTestListeningHide) el.chkPreTestListeningHide.checked = state.listeningHideText;
    state.listeningPeekQuestionId = null;

    updateListeningHideInExamButton();
    const currentQ = state.questions[state.currentIndex];
    if (currentQ) renderOptions(currentQ);

    showToast(state.listeningHideText 
      ? '🙈 Đã BẬT ẩn chữ đáp án (chỉ để lại A, B, C, D)!' 
      : '👁️ Đã HIỆN chữ đáp án đầy đủ!');
  }

  function updateListeningHideInExamButton() {
    if (!el.btnToggleListeningHideInExam) return;
    if (state.currentSkill === 'listening') {
      el.btnToggleListeningHideInExam.style.display = 'inline-flex';
      if (el.listeningHideLabel) {
        el.listeningHideLabel.textContent = state.listeningHideText ? 'Chỉ A B C D' : 'Hiện đủ chữ';
      }
      if (el.listeningHideIcon) {
        el.listeningHideIcon.textContent = state.listeningHideText ? '🙈' : '👁️';
      }
      if (state.listeningHideText) {
        el.btnToggleListeningHideInExam.classList.add('active');
      } else {
        el.btnToggleListeningHideInExam.classList.remove('active');
      }
    } else {
      el.btnToggleListeningHideInExam.style.display = 'none';
    }
  }

  function togglePeekListeningCurrentQuestion() {
    const q = state.questions[state.currentIndex];
    if (!q) return;
    if (state.listeningPeekQuestionId === q.id) {
      state.listeningPeekQuestionId = null;
    } else {
      state.listeningPeekQuestionId = q.id;
    }
    renderOptions(q);
  }

  // =========================================================================
  // QUESTION PALETTE SETUP
  // =========================================================================
  function setupPalette() {
    el.gridPart1.innerHTML = '';
    el.gridPart2.innerHTML = '';
    el.gridPart3.innerHTML = '';

    const p1Container = document.getElementById('groupPart1');
    const p2Container = document.getElementById('groupPart2');
    const p3Container = document.getElementById('groupPart3');

    // Update Palette Titles based on skill
    if (state.currentSkill === 'listening') {
      el.titleGroupPart1.textContent = 'Part 1: Photographs';
      el.titleGroupPart2.textContent = 'Part 2: Q & A';
      el.titleGroupPart3.textContent = 'Part 3: Conversations';
    } else {
      el.titleGroupPart1.textContent = 'Part 1: Điền vào câu (Part 5)';
      el.titleGroupPart2.textContent = 'Part 2: Điền đoạn văn (Part 6)';
      el.titleGroupPart3.textContent = 'Part 3: Đọc hiểu (Part 7)';
    }

    let hasP1 = false, hasP2 = false, hasP3 = false;

    state.questions.forEach((q, idx) => {
      const btn = document.createElement('button');
      btn.className = 'palette-btn';
      btn.textContent = q.questionNum;
      btn.dataset.index = idx;
      btn.addEventListener('click', () => {
        loadQuestion(idx);
      });

      if (q.part === 1) {
        el.gridPart1.appendChild(btn);
        hasP1 = true;
      } else if (q.part === 2) {
        el.gridPart2.appendChild(btn);
        hasP2 = true;
      } else {
        el.gridPart3.appendChild(btn);
        hasP3 = true;
      }
    });

    p1Container.style.display = hasP1 ? 'block' : 'none';
    p2Container.style.display = hasP2 ? 'block' : 'none';
    p3Container.style.display = hasP3 ? 'block' : 'none';

    updatePaletteStatus();
  }

  function updatePaletteStatus() {
    const buttons = document.querySelectorAll('#gridPart1 .palette-btn, #gridPart2 .palette-btn, #gridPart3 .palette-btn');
    let answeredCount = 0;

    buttons.forEach(btn => {
      const idx = parseInt(btn.dataset.index, 10);
      const q = state.questions[idx];

      btn.classList.remove('current', 'answered', 'flagged');

      if (idx === state.currentIndex) {
        btn.classList.add('current');
      }

      if (state.userAnswers[q.id]) {
        btn.classList.add('answered');
        answeredCount++;
      }

      if (state.flaggedQuestions[q.id]) {
        btn.classList.add('flagged');
      }
    });

    if (state.mode === 'study') {
      el.answeredCounterText.textContent = `Đang học: Câu ${state.currentIndex + 1}/${state.questions.length}`;
    } else {
      el.answeredCounterText.textContent = `Đã làm: ${answeredCount}/${state.questions.length}`;
    }
  }

  // =========================================================================
  // LOAD QUESTION
  // =========================================================================
  function loadQuestion(index) {
    if (index < 0 || index >= state.questions.length) return;

    state.currentIndex = index;
    const q = state.questions[index];

    // 1. Header Pills
    const skillName = (q.skill === 'reading' || state.currentSkill === 'reading') ? 'Reading B1' : 'Listening';
    el.qNumberPill.textContent = `Câu ${q.questionNum} / ${state.questions.length} (Test ${q.test})`;
    el.qPartPill.textContent = `Part ${q.part}`;
    el.qSkillPill.textContent = skillName;
    if (el.qShufflePill) {
      el.qShufflePill.style.display = q.isOptionsShuffled ? 'inline-flex' : 'none';
    }
    updateShuffleInExamButton();
    updateListeningHideInExamButton();
    state.listeningPeekQuestionId = null;

    // 2. Flag State
    if (state.flaggedQuestions[q.id]) {
      el.btnFlagQuestion.classList.add('flagged');
      el.flagBtnText.textContent = 'Đã cờ';
    } else {
      el.btnFlagQuestion.classList.remove('flagged');
      el.flagBtnText.textContent = 'Đánh dấu';
    }

    // 3. Audio & Passage Handling
    if (q.skill === 'reading' || state.currentSkill === 'reading') {
      // Reading Mode: Hide Audio Bar
      el.questionAudioBar.style.display = 'none';
      stopAudio();

      // Show Reading Passage if present (Part 2 or Part 3)
      if (q.passage) {
        el.qPassageContainer.style.display = 'block';
        el.qPassageContent.innerHTML = q.passage;
      } else {
        el.qPassageContainer.style.display = 'none';
        el.qPassageContent.innerHTML = '';
      }

      // Hide Part 1 Image
      el.qImageContainer.style.display = 'none';
      el.qImage.src = '';
    } else {
      // Listening Mode: Show Audio Bar
      el.questionAudioBar.style.display = 'flex';
      el.qPassageContainer.style.display = 'none';
      loadQuestionAudio(q);

      // Part 1 Image
      if (q.image) {
        el.qImageContainer.style.display = 'block';
        el.qImage.src = q.image;
      } else {
        el.qImageContainer.style.display = 'none';
        el.qImage.src = '';
      }
    }

    // 4. Prompt Text
    el.qPrompt.innerHTML = q.prompt || `Câu hỏi ${q.questionNum}`;

    // 5. Options
    renderOptions(q);

    // 6. Explanation in Practice or Study Mode
    if (state.mode === 'study') {
      showPracticeExplanation(q);
    } else if (state.mode === 'practice' && state.userAnswers[q.id]) {
      showPracticeExplanation(q);
    } else {
      el.qExplanationBox.style.display = 'none';
    }

    // 7. Navigation Buttons State
    el.btnPrevQuestion.disabled = (index === 0);
    el.btnNextQuestion.disabled = (index === state.questions.length - 1);

    // 8. Update Palette Highlights
    updatePaletteStatus();
  }

  function renderOptions(q) {
    el.qOptionsContainer.innerHTML = '';
    const selected = state.userAnswers[q.id];
    const isListening = (state.currentSkill === 'listening' || q.skill === 'listening');
    const isPeeked = (state.listeningPeekQuestionId === q.id);
    const shouldHideText = (state.mode !== 'study') && isListening && state.listeningHideText && !isPeeked;

    // Handle inline listening hide banner
    if (el.listeningHideBanner) {
      if (state.mode !== 'study' && isListening && state.listeningHideText) {
        el.listeningHideBanner.style.display = 'flex';
        if (el.btnPeekListening) {
          el.btnPeekListening.textContent = isPeeked ? '🙈 Ẩn lại chữ' : '👁️ Xem chữ câu này';
        }
      } else {
        el.listeningHideBanner.style.display = 'none';
      }
    }

    q.options.forEach(opt => {
      const item = document.createElement('div');
      item.className = 'option-item';
      if (shouldHideText) {
        item.classList.add('hide-listening-text');
      }
      if (selected === opt.key) {
        item.classList.add('selected');
      }

      if (state.mode === 'study') {
        if (opt.key === q.correctAnswer) {
          item.classList.add('correct', 'study-correct');
        }
      } else if (state.mode === 'practice' && selected) {
        if (opt.key === q.correctAnswer) {
          item.classList.add('correct');
        } else if (opt.key === selected) {
          item.classList.add('incorrect');
        }
      }

      if (state.mode === 'study') {
        const isCorrect = (opt.key === q.correctAnswer);
        const tag = isCorrect ? '<span class="study-correct-tag">✅ Đáp án chuẩn</span>' : '';
        item.innerHTML = `
          <div class="option-key">${opt.key}</div>
          <div class="option-text">${opt.text} ${tag}</div>
        `;
      } else if (shouldHideText) {
        item.innerHTML = `
          <div class="option-key">${opt.key}</div>
          <div class="option-text"><span class="hidden-text-subtle">Lắng nghe audio & chọn (${opt.key})</span></div>
        `;
      } else {
        item.innerHTML = `
          <div class="option-key">${opt.key}</div>
          <div class="option-text">${opt.text}</div>
        `;
      }

      item.addEventListener('click', () => {
        selectOption(q, opt.key);
      });

      el.qOptionsContainer.appendChild(item);
    });
  }

  function selectOption(q, key) {
    state.userAnswers[q.id] = key;
    renderOptions(q);
    updatePaletteStatus();

    if (state.mode === 'practice' || state.mode === 'study') {
      showPracticeExplanation(q);
    }
  }

  function showPracticeExplanation(q) {
    el.qExplanationBox.style.display = 'block';
    el.qExplanationContent.innerHTML = q.explanation || 'Không có giải thích chi tiết.';
  }

  // =========================================================================
  // AUDIO CONTROLS (LISTENING)
  // =========================================================================
  function loadQuestionAudio(q) {
    if (!q.audio) {
      el.currentAudioLabel.textContent = 'Không có audio cho câu này';
      return;
    }

    el.currentAudioLabel.textContent = `Phát: ${q.audio.replace('media/', '')}`;
    el.audioPlayer.src = q.audio;
    el.audioPlayer.playbackRate = parseFloat(el.audioSpeedSelect.value || '1.0');
    el.audioPlayer.play().catch(() => {
      el.playPauseIcon.textContent = '▶️';
    });
  }

  function toggleAudioPlay() {
    if (el.audioPlayer.paused) {
      el.audioPlayer.play().catch(e => console.warn(e));
    } else {
      el.audioPlayer.pause();
    }
  }

  function stopAudio() {
    el.audioPlayer.pause();
    el.audioPlayer.currentTime = 0;
    el.playPauseIcon.textContent = '▶️';
    if (el.audioWaveAnim) el.audioWaveAnim.classList.remove('playing');
  }

  function seekAudio(seconds) {
    if (el.audioPlayer.duration) {
      el.audioPlayer.currentTime = Math.max(0, Math.min(el.audioPlayer.duration, el.audioPlayer.currentTime + seconds));
    }
  }

  function updateAudioProgress() {
    if (el.audioPlayer.duration) {
      const pct = (el.audioPlayer.currentTime / el.audioPlayer.duration) * 100;
      el.audioSeekBar.value = pct;
      el.audioCurrentTime.textContent = formatTime(el.audioPlayer.currentTime);
    }
  }

  // =========================================================================
  // TIMER (EXAM MODE)
  // =========================================================================
  function startTimer(durationSeconds) {
    stopTimer();
    state.timerSeconds = durationSeconds;
    el.timerCountdown.textContent = formatMinutesSeconds(state.timerSeconds);

    state.timerInterval = setInterval(() => {
      state.timerSeconds--;
      state.timeSpentSeconds++;
      el.timerCountdown.textContent = formatMinutesSeconds(state.timerSeconds);

      if (state.timerSeconds <= 0) {
        stopTimer();
        alert('Hết giờ làm bài! Hệ thống sẽ tự động thu bài và chấm điểm.');
        submitExam();
      }
    }, 1000);
  }

  function stopTimer() {
    if (state.timerInterval) {
      clearInterval(state.timerInterval);
      state.timerInterval = null;
    }
  }

  // =========================================================================
  // NAVIGATION & SHORTCUTS
  // =========================================================================
  function goToPrevQuestion() {
    if (state.currentIndex > 0) {
      loadQuestion(state.currentIndex - 1);
    }
  }

  function goToNextQuestion() {
    if (state.currentIndex < state.questions.length - 1) {
      loadQuestion(state.currentIndex + 1);
    }
  }

  function toggleFlagCurrentQuestion() {
    const q = state.questions[state.currentIndex];
    state.flaggedQuestions[q.id] = !state.flaggedQuestions[q.id];
    loadQuestion(state.currentIndex);
  }

  function handleKeyboardShortcuts(e) {
    if (state.activeScreen === 'translation') {
      if (e.key === 'Enter' && e.ctrlKey) {
        revealTranslation();
      } else if (e.key === 'ArrowLeft' && e.altKey) {
        if (state.transIndex > 0) loadTranslationCard(state.transIndex - 1);
      } else if (e.key === 'ArrowRight' && e.altKey) {
        if (state.transIndex < state.transQuestions.length - 1) loadTranslationCard(state.transIndex + 1);
      }
      return;
    }

    if (!el.screenExam.classList.contains('active')) return;
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;

    const q = state.questions[state.currentIndex];
    if (!q) return;

    const key = e.key.toUpperCase();
    const keyMap = { '1': 'A', '2': 'B', '3': 'C', '4': 'D' };
    const optionChoice = keyMap[key] || key;

    if (['A', 'B', 'C', 'D'].includes(optionChoice)) {
      const exists = q.options.some(o => o.key === optionChoice);
      if (exists) {
        e.preventDefault();
        selectOption(q, optionChoice);
      }
    } else if (e.key === ' ' && state.currentSkill === 'listening') {
      e.preventDefault();
      toggleAudioPlay();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      goToPrevQuestion();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      goToNextQuestion();
    } else if (key === 'F') {
      e.preventDefault();
      toggleFlagCurrentQuestion();
    }
  }

  // =========================================================================
  // SUBMISSION & GRADING
  // =========================================================================
  function switchToExamFromStudy() {
    const isTest = (typeof state.testId === 'number');
    const skillName = (state.currentSkill === 'reading') ? 'Reading B1' : 'Listening';
    const targetLabel = isTest ? `${skillName} Test ${state.testId}` : `${skillName} Part ${state.testId.replace('part_', '')}`;
    const confirmed = confirm(`Bạn đã hoàn tất ôn tập ${targetLabel}?\n\nNhấn "OK" để bắt đầu làm bài Thi Thử (tính giờ 45 phút) để tự kiểm tra kiến thức ngay bây giờ.`);
    if (!confirmed) return;

    setMode('exam');
    if (isTest) {
      startTest(state.testId);
    } else {
      const partNum = parseInt(state.testId.replace('part_', ''), 10);
      startPartTest(partNum);
    }
    showToast('🚀 Bắt đầu làm bài Thi Thử tính giờ! Chúc bạn làm bài tốt!');
  }

  function promptSubmitExam() {
    if (state.mode === 'study') {
      switchToExamFromStudy();
      return;
    }

    const total = state.questions.length;
    let answered = 0;
    state.questions.forEach(q => {
      if (state.userAnswers[q.id]) answered++;
    });

    const unanswered = total - answered;

    if (unanswered > 0) {
      el.modalWarningText.innerHTML = `Bạn vẫn còn <strong>${unanswered}</strong> câu chưa làm. Bạn có chắc chắn muốn nộp bài để xem điểm số ngay bây giờ?`;
    } else {
      el.modalWarningText.innerHTML = `Bạn đã hoàn thành <strong>${answered}/${total}</strong> câu hỏi. Bạn đã sẵn sàng nộp bài và xem bảng điểm?`;
    }

    el.confirmModal.classList.add('active');
  }

  function submitExam() {
    el.confirmModal.classList.remove('active');
    stopTimer();
    stopAudio();

    calculateAndRenderScore();
    showScreen('score');
  }

  function calculateAndRenderScore() {
    let correctCount = 0;
    let p1Correct = 0, p1Total = 0;
    let p2Correct = 0, p2Total = 0;
    let p3Correct = 0, p3Total = 0;

    state.questions.forEach(q => {
      const userAns = state.userAnswers[q.id];
      const isRight = (userAns && userAns === q.correctAnswer);

      if (isRight) correctCount++;

      if (q.part === 1) {
        p1Total++;
        if (isRight) p1Correct++;
      } else if (q.part === 2) {
        p2Total++;
        if (isRight) p2Correct++;
      } else {
        p3Total++;
        if (isRight) p3Correct++;
      }
    });

    const total = state.questions.length;
    const accuracy = ((correctCount / total) * 100).toFixed(1);

    // Calculate Scaled Score
    const scaledScore = (state.currentSkill === 'listening') 
      ? estimateToeicListeningScore(correctCount, total)
      : estimateToeicReadingScore(correctCount, total);

    el.scoreEstimated.textContent = scaledScore;
    el.correctCountDisplay.textContent = `${correctCount} / ${total}`;
    el.accuracyPercentage.textContent = `${accuracy}%`;
    el.timeSpentDisplay.textContent = formatMinutesSeconds(state.timeSpentSeconds || 60);

    const skillTitle = (state.currentSkill === 'listening') ? 'TOEIC Listening' : 'TOEIC Reading B1';

    if (accuracy >= 85) {
      el.scoreTitle.textContent = `🎉 Xuất Sắc! Điểm Số ${skillTitle} Rất Cao!`;
      el.scoreSubText.textContent = 'Bạn đã nắm vững kiến thức ngữ pháp và phản xạ bài thi!';
    } else if (accuracy >= 70) {
      el.scoreTitle.textContent = `👏 Rất Tốt! Đạt Chuẩn ${skillTitle}!`;
      el.scoreSubText.textContent = 'Xem lại một số câu làm sai để hoàn thiện tối đa điểm số!';
    } else {
      el.scoreTitle.textContent = `💪 Cố Lên! Tiếp Tục Luyện Tập ${skillTitle}!`;
      el.scoreSubText.textContent = 'Hãy xem lại danh sách các câu làm sai bên dưới để rút kinh nghiệm từ lời giải!';
    }

    // Set Breakdown Labels based on skill
    if (state.currentSkill === 'listening') {
      el.bPart1Label.textContent = 'Part 1';
      el.bPart1Sub.textContent = 'Mô tả tranh';
      el.bPart2Label.textContent = 'Part 2';
      el.bPart2Sub.textContent = 'Hỏi & Đáp';
      el.bPart3Label.textContent = 'Part 3';
      el.bPart3Sub.textContent = 'Đoạn hội thoại';
    } else {
      el.bPart1Label.textContent = 'Part 1 (P5)';
      el.bPart1Sub.textContent = 'Điền vào câu';
      el.bPart2Label.textContent = 'Part 2 (P6)';
      el.bPart2Sub.textContent = 'Điền đoạn văn';
      el.bPart3Label.textContent = 'Part 3 (P7)';
      el.bPart3Sub.textContent = 'Đọc hiểu';
    }

    if (p1Total > 0) {
      el.p1ScoreText.textContent = `${p1Correct}/${p1Total} câu (${Math.round((p1Correct/p1Total)*100)}%)`;
      el.p1BarFill.style.width = `${(p1Correct/p1Total)*100}%`;
    }
    if (p2Total > 0) {
      el.p2ScoreText.textContent = `${p2Correct}/${p2Total} câu (${Math.round((p2Correct/p2Total)*100)}%)`;
      el.p2BarFill.style.width = `${(p2Correct/p2Total)*100}%`;
    }
    if (p3Total > 0) {
      el.p3ScoreText.textContent = `${p3Correct}/${p3Total} câu (${Math.round((p3Correct/p3Total)*100)}%)`;
      el.p3BarFill.style.width = `${(p3Correct/p3Total)*100}%`;
    }

    const wrongCount = total - correctCount;
    el.cntFilterAll.textContent = total;
    el.cntFilterWrong.textContent = wrongCount;
    el.cntFilterRight.textContent = correctCount;

    let unansweredCount = 0;
    state.questions.forEach(q => {
      if (!state.userAnswers[q.id]) unansweredCount++;
    });
    el.cntFilterUnanswered.textContent = unansweredCount;

    renderReviewList();
  }

  function estimateToeicListeningScore(correct, total) {
    if (total === 70) {
      const factor = 100 / 70;
      const raw100 = Math.min(100, Math.round(correct * factor));
      return convert100ToToeicScaled(raw100);
    } else {
      const ratio = correct / total;
      return Math.round(ratio * 490) + 5;
    }
  }

  function estimateToeicReadingScore(correct, total) {
    if (total === 50) {
      const factor = 100 / 50;
      const raw100 = Math.min(100, Math.round(correct * factor));
      return convert100ToToeicScaled(raw100);
    } else {
      const ratio = correct / total;
      return Math.round(ratio * 490) + 5;
    }
  }

  function convert100ToToeicScaled(score100) {
    if (score100 >= 96) return 495;
    if (score100 >= 91) return 480;
    if (score100 >= 86) return 455;
    if (score100 >= 81) return 430;
    if (score100 >= 76) return 400;
    if (score100 >= 71) return 375;
    if (score100 >= 66) return 350;
    if (score100 >= 61) return 325;
    if (score100 >= 56) return 295;
    if (score100 >= 51) return 270;
    if (score100 >= 46) return 240;
    if (score100 >= 41) return 210;
    if (score100 >= 36) return 180;
    if (score100 >= 31) return 150;
    if (score100 >= 26) return 120;
    if (score100 >= 21) return 90;
    return 50;
  }

  function renderReviewList() {
    el.reviewQuestionsList.innerHTML = '';
    const filter = state.filterReview;

    state.questions.forEach((q, idx) => {
      const userAns = state.userAnswers[q.id];
      const isCorrect = (userAns && userAns === q.correctAnswer);
      const isUnanswered = !userAns;

      if (filter === 'wrong' && isCorrect) return;
      if (filter === 'right' && !isCorrect) return;
      if (filter === 'unanswered' && !isUnanswered) return;

      const card = document.createElement('div');
      card.className = `review-item-card ${isCorrect ? 'is-correct' : (isUnanswered ? 'is-unanswered' : 'is-incorrect')}`;

      let tagHtml = '';
      if (isCorrect) {
        tagHtml = `<span class="review-status-tag correct">✅ Đúng</span>`;
      } else if (isUnanswered) {
        tagHtml = `<span class="review-status-tag unanswered">⚪ Chưa làm</span>`;
      } else {
        tagHtml = `<span class="review-status-tag incorrect">❌ Sai (Bạn chọn ${userAns})</span>`;
      }

      const imgHtml = q.image ? `<div class="q-image-container" style="margin-bottom:12px;"><img src="${q.image}" style="max-height:220px;" alt="Hình ảnh"></div>` : '';

      const audioHtml = q.audio ? `
        <div class="review-audio-inline">
          <audio controls preload="none" style="width:100%; height:36px;">
            <source src="${q.audio}" type="audio/mpeg">
          </audio>
        </div>` : '';

      const passageHtml = q.passage ? `
        <div class="q-passage-container" style="margin-bottom:12px; font-size:13.5px;">
          ${q.passage}
        </div>` : '';

      const skillTag = (q.skill === 'reading') ? 'Reading' : 'Listening';

      card.innerHTML = `
        <div class="review-item-top">
          <span class="review-q-title">Câu ${q.questionNum} (Part ${q.part} - ${skillTag} Test ${q.test})</span>
          ${tagHtml}
        </div>
        ${passageHtml}
        ${imgHtml}
        <div class="q-prompt" style="font-size:14.5px; margin-bottom:12px;">${q.prompt}</div>
        ${audioHtml}
        <div class="review-answers-compare">
          <div>Bạn chọn: <strong>${userAns ? `(${userAns})` : 'Chưa chọn'}</strong></div>
          <div style="color:var(--success);">Đáp án đúng: <strong>(${q.correctAnswer})</strong></div>
        </div>
        <div class="q-explanation-box" style="margin-top:10px;">
          <div class="explanation-body">${q.explanation || 'Không có giải thích.'}</div>
        </div>
      `;

      el.reviewQuestionsList.appendChild(card);
    });

    if (el.reviewQuestionsList.children.length === 0) {
      el.reviewQuestionsList.innerHTML = `<div style="text-align:center; padding:30px; color:var(--text-muted);">Không có câu hỏi nào thỏa mãn bộ lọc này.</div>`;
    }
  }

  // =========================================================================
  // TRANSLATION PRACTICE MODULE (480 QUESTIONS)
  // =========================================================================
  function initTranslationState() {
    filterTranslationData();
  }

  function openTranslationMode() {
    stopAudio();
    stopTransAudio();
    showScreen('translation');
    filterTranslationData();
  }

  function setTransDirection(dir) {
    state.transDirection = dir;
    if (dir === 'en-vi') {
      el.btnDirEnVi.classList.add('active');
      el.btnDirViEn.classList.remove('active');
    } else {
      el.btnDirViEn.classList.add('active');
      el.btnDirEnVi.classList.remove('active');
    }
    loadTranslationCard(state.transIndex);
  }

  function filterTranslationData() {
    const rawData = window.TRANSLATION_DATA || [];
    let filtered = rawData;

    // Filter by skill
    if (state.transSkill !== 'all') {
      filtered = filtered.filter(item => item.skill === state.transSkill);
    }

    // Filter by test
    if (state.transTest !== 'all') {
      const tNum = parseInt(state.transTest, 10);
      filtered = filtered.filter(item => item.test === tNum);
    }

    // Filter by part
    if (state.transPart !== 'all') {
      const pNum = parseInt(state.transPart, 10);
      filtered = filtered.filter(item => item.part === pNum);
    }

    state.transQuestions = filtered;
    state.transIndex = 0;

    setupTranslationPalette();
    loadTranslationCard(0);
  }

  function setupTranslationPalette() {
    el.transPaletteGrid.innerHTML = '';

    state.transQuestions.forEach((item, idx) => {
      const btn = document.createElement('button');
      btn.className = 'palette-btn';
      btn.textContent = idx + 1;
      btn.dataset.index = idx;
      btn.addEventListener('click', () => {
        loadTranslationCard(idx);
      });
      el.transPaletteGrid.appendChild(btn);
    });

    updateTranslationPalette();
  }

  function updateTranslationPalette() {
    const buttons = el.transPaletteGrid.querySelectorAll('.palette-btn');
    let ratedCount = 0;

    buttons.forEach(btn => {
      const idx = parseInt(btn.dataset.index, 10);
      const item = state.transQuestions[idx];

      btn.classList.remove('current', 'trans-hard', 'trans-good', 'trans-easy');

      if (idx === state.transIndex) {
        btn.classList.add('current');
      }

      const rating = state.transRatings[item.id];
      if (rating) {
        btn.classList.add(`trans-${rating}`);
        ratedCount++;
      }
    });

    el.transProgressText.textContent = `Tiến độ: ${ratedCount} / ${state.transQuestions.length} câu`;
  }

  function loadTranslationCard(index) {
    if (!state.transQuestions.length) {
      el.transSourceText.textContent = 'Không có câu hỏi nào thỏa mãn bộ lọc.';
      return;
    }

    if (index < 0 || index >= state.transQuestions.length) return;

    state.transIndex = index;
    const item = state.transQuestions[index];

    const skillLabel = (item.skill === 'reading') ? 'Reading' : 'Listening';
    el.transNumberPill.textContent = `Câu ${index + 1} / ${state.transQuestions.length}`;
    el.transPartPill.textContent = `Part ${item.part}`;
    el.transContextPill.textContent = `${skillLabel} Test ${item.test}`;

    // Image for Part 1 (Listening)
    if (item.image) {
      el.transImageContainer.style.display = 'block';
      el.transImage.src = item.image;
    } else {
      el.transImageContainer.style.display = 'none';
      el.transImage.src = '';
    }

    // Direction Setup
    if (state.transDirection === 'en-vi') {
      el.transSourceLabel.textContent = '🇬🇧 CÂU TIẾNG ANH CẦN DỊCH:';
      el.transSourceText.textContent = item.en;
      el.transTargetLabel.textContent = '🇻🇳 BẢN DỊCH CHUẨN TIẾNG VIỆT:';
      el.transTargetText.textContent = item.vi;
    } else {
      el.transSourceLabel.textContent = '🇻🇳 CÂU TIẾNG VIỆT CẦN DỊCH SANG ANH:';
      el.transSourceText.textContent = item.vi;
      el.transTargetLabel.textContent = '🇬🇧 CÂU TIẾNG ANH CHUẨN:';
      el.transTargetText.textContent = item.en;
    }

    // Audio setup (if available)
    if (item.audio) {
      transAudio.src = item.audio;
      transAudio.playbackRate = parseFloat(el.transAudioSpeed.value || '1.0');
      el.btnTransAudioPlay.style.display = 'inline-flex';
      el.btnTransAudioPlay.textContent = '▶️ Nghe Audio';
    } else {
      el.btnTransAudioPlay.style.display = 'none';
    }

    // Reset user input and reveal box
    el.transUserInput.value = '';
    el.transHintBox.style.display = 'none';
    el.transRevealBox.style.display = 'none';
    el.btnToggleHint.textContent = '💡 Hiện Gợi Ý Từ Vựng';

    // Populate Hints
    el.transHintKeywords.innerHTML = '';
    if (item.vocabulary && item.vocabulary.length) {
      item.vocabulary.forEach(v => {
        const chip = document.createElement('span');
        chip.className = 'hint-keyword-item';
        chip.textContent = `${v.word}: ${v.meaning}`;
        el.transHintKeywords.appendChild(chip);
      });
      el.btnToggleHint.style.display = 'inline-flex';
    } else {
      el.btnToggleHint.style.display = 'none';
    }

    // Populate Vocabulary Chips
    el.transVocabChips.innerHTML = '';
    if (item.vocabulary && item.vocabulary.length) {
      el.transVocabSection.style.display = 'block';
      item.vocabulary.forEach(v => {
        const chip = document.createElement('div');
        chip.className = 'vocab-chip';
        chip.innerHTML = `<span class="chip-word">${v.word}</span> <span class="chip-meaning">→ ${v.meaning}</span>`;
        el.transVocabChips.appendChild(chip);
      });
    } else {
      el.transVocabSection.style.display = 'none';
    }

    // Populate Grammar / Technique
    if (item.grammar) {
      el.transGrammarSection.style.display = 'block';
      el.transGrammarContent.textContent = item.grammar;
    } else {
      el.transGrammarSection.style.display = 'none';
    }

    // Self rating state
    const currentRating = state.transRatings[item.id];
    document.querySelectorAll('.rating-btn').forEach(btn => {
      btn.classList.remove('active');
      if (currentRating && btn.dataset.rating === currentRating) {
        btn.classList.add('active');
      }
    });

    // Navigation buttons state
    el.btnTransPrev.disabled = (index === 0);
    el.btnTransNext.disabled = (index === state.transQuestions.length - 1);

    updateTranslationPalette();
  }

  function toggleTransAudio() {
    if (!transAudio.src) return;
    if (transAudio.paused) {
      transAudio.playbackRate = parseFloat(el.transAudioSpeed.value || '1.0');
      transAudio.play().then(() => {
        el.btnTransAudioPlay.textContent = '⏸️ Đang Phát...';
      }).catch(e => console.warn(e));
    } else {
      transAudio.pause();
      el.btnTransAudioPlay.textContent = '▶️ Nghe Audio';
    }
  }

  function stopTransAudio() {
    transAudio.pause();
    transAudio.currentTime = 0;
    if (el.btnTransAudioPlay) el.btnTransAudioPlay.textContent = '▶️ Nghe Audio';
  }

  transAudio.addEventListener('ended', () => {
    if (el.btnTransAudioPlay) el.btnTransAudioPlay.textContent = '▶️ Nghe Audio';
  });

  function toggleTransHint() {
    if (el.transHintBox.style.display === 'none') {
      el.transHintBox.style.display = 'block';
      el.btnToggleHint.textContent = '🙈 Ẩn Gợi Ý Từ Vựng';
    } else {
      el.transHintBox.style.display = 'none';
      el.btnToggleHint.textContent = '💡 Hiện Gợi Ý Từ Vựng';
    }
  }

  function revealTranslation() {
    el.transRevealBox.style.display = 'block';
    el.transRevealBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function rateCurrentTranslation(rating) {
    const item = state.transQuestions[state.transIndex];
    if (!item) return;

    state.transRatings[item.id] = rating;
    localStorage.setItem('toeic_trans_ratings', JSON.stringify(state.transRatings));

    document.querySelectorAll('.rating-btn').forEach(btn => {
      btn.classList.remove('active');
      if (btn.dataset.rating === rating) btn.classList.add('active');
    });

    updateTranslationPalette();
  }

  // =========================================================================
  // WRITING PRACTICE MODULE (PARAGRAPHS & 24 Q&A)
  // =========================================================================
  function initWritingModule() {
    setupWritingPalette();
    renderParagraphTopicPills();
    renderQACategories();
    loadParagraphTopic(state.writingParagraphIndex);
  }

  function openWritingMode() {
    stopAudio();
    stopTransAudio();
    showScreen('writing');
    initWritingModule();
  }

  function switchWritingSubtab(subtab) {
    state.writingSubtab = subtab;
    if (subtab === 'paragraph') {
      el.btnWritingSubtabParagraph.classList.add('active');
      el.btnWritingSubtabQA.classList.remove('active');
      el.viewWritingParagraph.style.display = 'block';
      el.viewWritingQA.style.display = 'none';
      el.writingPaletteTitle.textContent = 'Đề Viết Đoạn Văn (2 Đề)';
      setupWritingPalette();
      loadParagraphTopic(state.writingParagraphIndex);
    } else {
      el.btnWritingSubtabQA.classList.add('active');
      el.btnWritingSubtabParagraph.classList.remove('active');
      el.viewWritingParagraph.style.display = 'none';
      el.viewWritingQA.style.display = 'block';
      el.writingPaletteTitle.textContent = 'Danh Sách Câu Hỏi (24 Câu)';
      setupWritingPalette();
      loadQAQuestion(state.writingQAIndex);
    }
  }

  function toggleWritingStructure() {
    state.writingStructureOpen = !state.writingStructureOpen;
    if (state.writingStructureOpen) {
      el.structureBodyContent.style.display = 'flex';
      el.structureToggleIcon.textContent = '▼';
    } else {
      el.structureBodyContent.style.display = 'none';
      el.structureToggleIcon.textContent = '▶';
    }
  }

  function getWritingParagraphs() {
    return (window.TOEIC_WRITING_DATA && window.TOEIC_WRITING_DATA.paragraphs) || [];
  }

  function getWritingQATopics() {
    return (window.TOEIC_WRITING_DATA && window.TOEIC_WRITING_DATA.qaTopics) || [];
  }

  function getAllQAQuestions() {
    const topics = getWritingQATopics();
    const list = [];
    topics.forEach(t => {
      (t.questions || []).forEach(q => {
        list.push({
          ...q,
          catId: t.id,
          categoryName: t.category,
          uniqueId: `${t.id}_q${q.num}`
        });
      });
    });
    return list;
  }

  function renderParagraphTopicPills() {
    const paras = getWritingParagraphs();
    el.paragraphTopicSelector.innerHTML = '';
    paras.forEach((p, idx) => {
      const btn = document.createElement('button');
      btn.className = `writing-topic-pill-btn ${idx === state.writingParagraphIndex ? 'active' : ''}`;
      const draft = state.writingParagraphDrafts[p.id] || '';
      const wCount = (draft.match(/\b[a-zA-Z0-9'-]+\b/g) || []).length;
      btn.innerHTML = `
        <span class="pill-topic-title">Đề ${idx + 1}: ${p.topic}</span>
        <span class="pill-topic-sub">${p.titleVi} • ${wCount > 0 ? `Đã viết <strong>${wCount}</strong> từ` : 'Chưa viết'}</span>
      `;
      btn.addEventListener('click', () => loadParagraphTopic(idx));
      el.paragraphTopicSelector.appendChild(btn);
    });
  }

  function loadParagraphTopic(index) {
    const paras = getWritingParagraphs();
    if (!paras.length || index < 0 || index >= paras.length) return;

    state.writingParagraphIndex = index;
    const topic = paras[index];

    // Update active state in pills
    document.querySelectorAll('.writing-topic-pill-btn').forEach((btn, idx) => {
      btn.classList.toggle('active', idx === index);
    });

    el.paragraphTargetBadge.textContent = `Mục tiêu: ${topic.targetWords}`;
    el.paragraphPromptTitle.textContent = topic.topic;
    el.paragraphPromptVi.textContent = topic.titleVi;

    // Structure Outline
    el.outlineOpeningText.textContent = topic.structure.opening;
    el.outlineBodyText.textContent = topic.structure.body;
    el.outlineConclusionText.textContent = topic.structure.conclusion;

    // Connectors list (Click to insert into textarea)
    el.paragraphConnectorsList.innerHTML = '';
    (topic.connectors || []).forEach(conn => {
      const chip = document.createElement('span');
      chip.className = 'helper-chip';
      chip.textContent = conn;
      chip.title = 'Click để chèn vào vị trí con trỏ trong bài viết';
      chip.addEventListener('click', () => insertTextAtCursor(el.paragraphTextarea, conn + ' '));
      el.paragraphConnectorsList.appendChild(chip);
    });

    // Vocabulary list (Click to insert)
    el.paragraphVocabList.innerHTML = '';
    (topic.vocabulary || []).forEach(v => {
      const chip = document.createElement('span');
      chip.className = 'helper-chip vocab-badge';
      chip.textContent = `${v.word}: ${v.meaning}`;
      chip.title = `Click để chèn từ '${v.word.replace(/\s*\([^)]*\)/g, '').trim()}' vào bài viết`;
      chip.addEventListener('click', () => {
        const cleanWord = v.word.replace(/\s*\([^)]*\)/g, '').trim();
        insertTextAtCursor(el.paragraphTextarea, cleanWord + ' ');
      });
      el.paragraphVocabList.appendChild(chip);
    });

    // Load user draft
    const savedDraft = state.writingParagraphDrafts[topic.id] || '';
    el.paragraphTextarea.value = savedDraft;
    updateParagraphWordCount();

    // Hide sample reveal initially
    el.paragraphSampleReveal.style.display = 'none';

    updateWritingPalette();
  }

  function insertTextAtCursor(textarea, text) {
    const start = textarea.selectionStart || 0;
    const end = textarea.selectionEnd || 0;
    const val = textarea.value;
    textarea.value = val.substring(0, start) + text + val.substring(end);
    textarea.selectionStart = textarea.selectionEnd = start + text.length;
    textarea.focus();
    if (textarea === el.paragraphTextarea) {
      updateParagraphWordCount();
    } else {
      updateQAWordCount();
    }
  }

  function updateParagraphWordCount() {
    const topic = getWritingParagraphs()[state.writingParagraphIndex];
    if (!topic) return;

    const val = el.paragraphTextarea.value;
    const words = (val.match(/\b[a-zA-Z0-9'-]+\b/g) || []);
    const count = words.length;
    const charCount = val.length;

    el.paraWordCountBadge.innerHTML = `<strong>${count}</strong> / ${topic.wordCount} từ`;
    el.paraCharCountBadge.textContent = `${charCount} ký tự`;

    // Status target badge
    const minTarget = (topic.id === 'p_travel') ? 50 : 80;
    const maxTarget = (topic.id === 'p_travel') ? 85 : 130;

    if (count === 0) {
      el.paraStatusBadge.className = 'stat-status-badge';
      el.paraStatusBadge.textContent = 'Chưa viết';
    } else if (count < minTarget) {
      el.paraStatusBadge.className = 'stat-status-badge under';
      el.paraStatusBadge.textContent = `Chưa đủ từ (còn thiếu ${minTarget - count} từ)`;
    } else if (count <= maxTarget) {
      el.paraStatusBadge.className = 'stat-status-badge good';
      el.paraStatusBadge.textContent = `Chuẩn độ dài B1 (${count} từ)`;
    } else {
      el.paraStatusBadge.className = 'stat-status-badge over';
      el.paraStatusBadge.textContent = `Đầy đủ ý (${count} từ)`;
    }

    // Auto-save draft
    state.writingParagraphDrafts[topic.id] = val;
    localStorage.setItem('toeic_writing_para_drafts', JSON.stringify(state.writingParagraphDrafts));
    showAutosaveNotice();
    updateWritingPalette();
  }

  function showAutosaveNotice() {
    if (!el.writingAutosaveIndicator) return;
    el.writingAutosaveIndicator.style.opacity = '1';
    el.writingAutosaveIndicator.textContent = '💾 Đã lưu nháp';
  }

  function revealParagraphSample() {
    const topic = getWritingParagraphs()[state.writingParagraphIndex];
    if (!topic) return;

    el.paragraphSampleReveal.style.display = 'block';
    el.sampleParaWordCountPill.textContent = `${topic.wordCount} từ`;
    el.sampleParaEnBox.textContent = topic.sampleEn;
    el.sampleParaViBox.textContent = topic.sampleVi;

    // Vocab grid
    el.sampleParaVocabGrid.innerHTML = '';
    (topic.vocabulary || []).forEach(v => {
      const chip = document.createElement('div');
      chip.className = 'vocab-chip';
      chip.innerHTML = `<span class="chip-word">${v.word}</span> <span class="chip-meaning">→ ${v.meaning}</span>`;
      el.sampleParaVocabGrid.appendChild(chip);
    });

    // Comparison analysis
    const userText = el.paragraphTextarea.value.toLowerCase();
    let foundVocabs = [];
    (topic.vocabulary || []).forEach(v => {
      const cleanWord = v.word.replace(/\s*\([^)]*\)/g, '').toLowerCase().trim();
      if (userText.includes(cleanWord)) {
        foundVocabs.push(cleanWord);
      }
    });

    let foundConnectors = [];
    (topic.connectors || []).forEach(c => {
      const cleanConn = c.replace(/\.\.\./g, '').toLowerCase().trim();
      if (userText.includes(cleanConn)) {
        foundConnectors.push(cleanConn);
      }
    });

    const totalKeyItems = (topic.vocabulary || []).length + (topic.connectors || []).length;
    const totalFound = foundVocabs.length + foundConnectors.length;
    const matchPct = Math.min(100, Math.round((totalFound / Math.max(1, totalKeyItems)) * 100));

    el.paragraphComparisonBox.innerHTML = `
      <div style="font-weight:700; color:var(--text-main); margin-bottom:6px;">📊 Đánh giá bài viết của bạn so với đề thi B1:</div>
      <div class="match-score-bar-wrap">
        <div class="match-score-bar-fill" style="width: ${matchPct}%;"></div>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:12.5px; color:var(--text-muted); margin-bottom:8px;">
        <span>Vận dụng từ vựng & cấu trúc: <strong>${totalFound}/${totalKeyItems} cụm từ</strong></span>
        <span>Độ phong phú: <strong>${matchPct}%</strong></span>
      </div>
      <div style="font-size:13px; line-height:1.5;">
        ${foundVocabs.length > 0 ? `✅ Bạn đã dùng từ vựng: <strong style="color:var(--success);">${foundVocabs.join(', ')}</strong>.<br>` : ''}
        ${foundConnectors.length > 0 ? `✅ Bạn đã sử dụng liên từ nối: <strong style="color:var(--primary);">${foundConnectors.join(', ')}</strong>.<br>` : ''}
        ${totalFound === 0 ? `💡 <em>Mẹo: Hãy thử kết hợp thêm các từ nối như "In addition", "In short", hoặc các từ vựng gợi ý ở trên để bài viết mượt mà và chuẩn B1 hơn!</em>` : '🌟 <em>Rất tốt! Bài viết của bạn đã liên kết mạch lạc và bám sát các ý trọng tâm.</em>'}
      </div>
    `;

    el.paragraphSampleReveal.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function renderQACategories() {
    const topics = getWritingQATopics();
    el.qaCategoryNav.innerHTML = '';

    const allBtn = document.createElement('button');
    allBtn.className = `qa-cat-btn ${state.writingQACategory === 'all' ? 'active' : ''}`;
    allBtn.textContent = '🌟 Tất cả 4 Chủ đề (24 câu)';
    allBtn.addEventListener('click', () => filterQACategory('all'));
    el.qaCategoryNav.appendChild(allBtn);

    topics.forEach(t => {
      const btn = document.createElement('button');
      btn.className = `qa-cat-btn ${state.writingQACategory === t.id ? 'active' : ''}`;
      btn.textContent = t.category;
      btn.addEventListener('click', () => filterQACategory(t.id));
      el.qaCategoryNav.appendChild(btn);
    });
  }

  function filterQACategory(catId) {
    state.writingQACategory = catId;
    document.querySelectorAll('.qa-cat-btn').forEach(btn => {
      if (catId === 'all') {
        btn.classList.toggle('active', btn.textContent.includes('Tất cả'));
      } else {
        btn.classList.toggle('active', btn.textContent.toLowerCase().includes(catId.replace('qa_', '')));
      }
    });

    const all = getAllQAQuestions();
    const firstIdx = (catId === 'all') ? 0 : all.findIndex(q => q.catId === catId);
    if (firstIdx !== -1) loadQAQuestion(firstIdx);
  }

  function loadQAQuestion(index) {
    const questions = getAllQAQuestions();
    if (!questions.length || index < 0 || index >= questions.length) return;

    state.writingQAIndex = index;
    const q = questions[index];

    el.qaNumberPill.textContent = `Câu ${index + 1} / ${questions.length}`;
    el.qaThemePill.textContent = q.categoryName.split(' ')[0];

    el.qaPromptEn.textContent = q.q;
    el.qaPromptVi.textContent = q.qVi;

    // Starters
    el.qaStarterChipsList.innerHTML = '';
    (q.starters || []).forEach(s => {
      const chip = document.createElement('span');
      chip.className = 'starter-chip';
      chip.textContent = s;
      chip.title = 'Click để chèn vào câu trả lời';
      chip.addEventListener('click', () => insertTextAtCursor(el.qaAnswerTextarea, s + ' '));
      el.qaStarterChipsList.appendChild(chip);
    });

    // Keywords
    el.qaKeywordChipsList.innerHTML = '';
    (q.keywords || []).forEach(k => {
      const chip = document.createElement('span');
      chip.className = 'keyword-chip';
      chip.textContent = k;
      el.qaKeywordChipsList.appendChild(chip);
    });

    // Load draft
    const saved = state.writingQADrafts[q.uniqueId] || '';
    el.qaAnswerTextarea.value = saved;
    updateQAWordCount();

    // Reset sample reveal
    el.qaSampleReveal.style.display = 'none';

    // Prev/Next buttons
    el.btnQAPrev.disabled = (index === 0);
    el.btnQANext.disabled = (index === questions.length - 1);

    updateWritingPalette();
  }

  function updateQAWordCount() {
    const questions = getAllQAQuestions();
    const q = questions[state.writingQAIndex];
    if (!q) return;

    const val = el.qaAnswerTextarea.value;
    const words = (val.match(/\b[a-zA-Z0-9'-]+\b/g) || []);
    const count = words.length;

    el.qaWordCountBadge.innerHTML = `<strong>${count}</strong> từ`;

    if (count > 0) {
      el.qaStatusPill.className = 'qa-status-pill done';
      el.qaStatusPill.textContent = 'Đã viết';
    } else {
      el.qaStatusPill.className = 'qa-status-pill';
      el.qaStatusPill.textContent = 'Chưa làm';
    }

    state.writingQADrafts[q.uniqueId] = val;
    localStorage.setItem('toeic_writing_qa_drafts', JSON.stringify(state.writingQADrafts));
    showAutosaveNotice();
    updateWritingPalette();
  }

  function revealQASample() {
    const questions = getAllQAQuestions();
    const q = questions[state.writingQAIndex];
    if (!q) return;

    el.qaSampleReveal.style.display = 'block';
    el.qaSampleEnBox.textContent = q.a;
    el.qaSampleViBox.textContent = q.aVi;

    // Match keywords
    const userText = el.qaAnswerTextarea.value.toLowerCase();
    const foundKeywords = [];
    (q.keywords || []).forEach(k => {
      const cleanWord = k.split('(')[0].trim().toLowerCase();
      if (userText.includes(cleanWord)) {
        foundKeywords.push(cleanWord);
      }
    });

    el.qaComparisonBox.innerHTML = `
      <div style="font-size:13px; line-height:1.5;">
        ${foundKeywords.length > 0 ? `✅ Bạn đã dùng từ khóa: <strong style="color:var(--success);">${foundKeywords.join(', ')}</strong>.<br>` : ''}
        💡 <em>Bản dịch chuẩn: ${q.aVi}</em>
      </div>
    `;

    el.qaSampleReveal.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function setupWritingPalette() {
    el.writingPaletteGrid.innerHTML = '';
    if (state.writingSubtab === 'paragraph') {
      const paras = getWritingParagraphs();
      paras.forEach((p, idx) => {
        const btn = document.createElement('button');
        btn.className = 'palette-btn';
        btn.style.width = '100%';
        btn.style.height = 'auto';
        btn.style.padding = '8px 12px';
        btn.style.textAlign = 'left';
        btn.style.fontSize = '13px';
        btn.style.lineHeight = '1.3';
        btn.textContent = `Đề ${idx + 1}: ${p.topic}`;
        btn.dataset.index = idx;
        btn.addEventListener('click', () => loadParagraphTopic(idx));
        el.writingPaletteGrid.appendChild(btn);
      });
    } else {
      const questions = getAllQAQuestions();
      questions.forEach((q, idx) => {
        const btn = document.createElement('button');
        btn.className = 'palette-btn';
        btn.textContent = idx + 1;
        btn.dataset.index = idx;
        btn.addEventListener('click', () => loadQAQuestion(idx));
        el.writingPaletteGrid.appendChild(btn);
      });
    }
    updateWritingPalette();
  }

  function updateWritingPalette() {
    const buttons = el.writingPaletteGrid.querySelectorAll('.palette-btn');
    if (state.writingSubtab === 'paragraph') {
      const paras = getWritingParagraphs();
      buttons.forEach(btn => {
        const idx = parseInt(btn.dataset.index, 10);
        const p = paras[idx];
        if (!p) return;
        btn.classList.remove('current', 'writing-done');
        if (idx === state.writingParagraphIndex) btn.classList.add('current');
        const draft = state.writingParagraphDrafts[p.id] || '';
        const wCount = (draft.match(/\b[a-zA-Z0-9'-]+\b/g) || []).length;
        if (wCount >= 40) btn.classList.add('writing-done');
      });
    } else {
      const questions = getAllQAQuestions();
      let answeredCount = 0;
      buttons.forEach(btn => {
        const idx = parseInt(btn.dataset.index, 10);
        const q = questions[idx];
        if (!q) return;
        btn.classList.remove('current', 'writing-done');
        if (idx === state.writingQAIndex) btn.classList.add('current');
        const draft = (state.writingQADrafts[q.uniqueId] || '').trim();
        if (draft.length > 0) {
          btn.classList.add('writing-done');
          answeredCount++;
        }
      });
      el.qaProgressSummary.textContent = `Tiến độ: ${answeredCount} / ${questions.length} câu đã viết`;
    }
  }

  function clearCurrentWritingDraft() {
    if (state.writingSubtab === 'paragraph') {
      const topic = getWritingParagraphs()[state.writingParagraphIndex];
      if (!topic) return;
      if (confirm(`Bạn có chắc muốn xóa bản nháp của đề "${topic.topic}"?`)) {
        el.paragraphTextarea.value = '';
        delete state.writingParagraphDrafts[topic.id];
        localStorage.setItem('toeic_writing_para_drafts', JSON.stringify(state.writingParagraphDrafts));
        updateParagraphWordCount();
        renderParagraphTopicPills();
      }
    } else {
      const q = getAllQAQuestions()[state.writingQAIndex];
      if (!q) return;
      if (confirm('Bạn có chắc muốn xóa câu trả lời cho câu này?')) {
        el.qaAnswerTextarea.value = '';
        delete state.writingQADrafts[q.uniqueId];
        localStorage.setItem('toeic_writing_qa_drafts', JSON.stringify(state.writingQADrafts));
        updateQAWordCount();
      }
    }
  }

  function resetAllWritingDrafts() {
    if (confirm('Bạn có chắc chắn muốn đặt lại và xóa TOÀN BỘ bài viết (cả 2 đề đoạn văn và 24 câu hỏi)?')) {
      state.writingParagraphDrafts = {};
      state.writingQADrafts = {};
      localStorage.removeItem('toeic_writing_para_drafts');
      localStorage.removeItem('toeic_writing_qa_drafts');
      if (state.writingSubtab === 'paragraph') {
        loadParagraphTopic(state.writingParagraphIndex);
        renderParagraphTopicPills();
      } else {
        loadQAQuestion(state.writingQAIndex);
      }
      alert('Đã xóa toàn bộ bản nháp luyện viết!');
    }
  }

  function speakText(text) {
    if (!('speechSynthesis' in window)) {
      alert('Trình duyệt của bạn không hỗ trợ Web Speech API để phát âm.');
      return;
    }
    window.speechSynthesis.cancel();
    if (!text || !text.trim()) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.95;

    const voices = window.speechSynthesis.getVoices();
    const enVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Samantha') || v.name.includes('David')));
    if (enVoice) utterance.voice = enVoice;

    window.speechSynthesis.speak(utterance);
  }

  // =========================================================================
  // QUESTION SEARCH & ANSWER EDITOR CONTROLLER
  // =========================================================================
  function applyAllOverrides() {
    const overrides = state.customOverrides;
    if (!overrides || typeof overrides !== 'object') return;

    if (Array.isArray(window.TOEIC_DATA)) {
      window.TOEIC_DATA.forEach(q => {
        if (overrides[q.id]) {
          const ov = overrides[q.id];
          if (ov.correctAnswer) q.correctAnswer = ov.correctAnswer;
          if (ov.explanation !== undefined) q.explanation = ov.explanation;
          q.isCustomEdited = true;
        }
      });
    }

    if (Array.isArray(window.TOEIC_READING_DATA)) {
      window.TOEIC_READING_DATA.forEach(q => {
        if (overrides[q.id]) {
          const ov = overrides[q.id];
          if (ov.correctAnswer) q.correctAnswer = ov.correctAnswer;
          if (ov.explanation !== undefined) q.explanation = ov.explanation;
          q.isCustomEdited = true;
        }
      });
    }
  }

  function getAllEditorQuestions() {
    const list = [];
    if (Array.isArray(window.TOEIC_DATA)) {
      window.TOEIC_DATA.forEach(q => {
        list.push({ ...q, skill: 'listening' });
      });
    }
    if (Array.isArray(window.TOEIC_READING_DATA)) {
      window.TOEIC_READING_DATA.forEach(q => {
        list.push({ ...q, skill: 'reading' });
      });
    }
    return list;
  }

  function openEditorMode() {
    stopAudio();
    stopTransAudio();
    stopEditorAudio();
    showScreen('editor');
    state.editorVisibleLimit = 20;
    renderEditorQuestions();
  }

  function stopEditorAudio() {
    if (editorAudio) {
      editorAudio.pause();
      editorAudio.currentTime = 0;
    }
    document.querySelectorAll('.btn-mini-audio').forEach(b => {
      b.textContent = '🔊 Nghe';
    });
  }

  function playEditorAudio(src, btnElement) {
    if (!src) return;
    if (editorAudio && !editorAudio.paused && editorAudio.src.endsWith(src)) {
      editorAudio.pause();
      if (btnElement) btnElement.textContent = '🔊 Nghe';
      return;
    }
    stopAudio();
    stopTransAudio();
    if (editorAudio) {
      editorAudio.pause();
    }
    editorAudio = new Audio(src);
    editorAudio.play().then(() => {
      document.querySelectorAll('.btn-mini-audio').forEach(b => b.textContent = '🔊 Nghe');
      if (btnElement) btnElement.textContent = '⏸️ Dừng';
    }).catch(e => console.warn(e));
    editorAudio.onended = () => {
      if (btnElement) btnElement.textContent = '🔊 Nghe';
    };
  }

  function renderEditorQuestions(appendOnly = false) {
    const allQuestions = getAllEditorQuestions();
    const query = (state.editorSearchQuery || '').trim().toLowerCase();
    const filterSkill = state.editorFilterSkill;
    const filterTest = state.editorFilterTest;
    const filterPart = state.editorFilterPart;
    const filterEdited = state.editorFilterEdited;

    const filtered = allQuestions.filter(q => {
      // Skill filter
      if (filterSkill !== 'all' && q.skill !== filterSkill) return false;
      // Test filter
      if (filterTest !== 'all' && q.test !== parseInt(filterTest, 10)) return false;
      // Part filter
      if (filterPart !== 'all' && q.part !== parseInt(filterPart, 10)) return false;
      // Edited filter
      const isEdited = !!state.customOverrides[q.id];
      if (filterEdited === 'edited' && !isEdited) return false;

      // Query filter
      if (query) {
        const idMatch = (q.id || '').toLowerCase().includes(query);
        const qNumMatch = String(q.questionNum) === query || `câu ${q.questionNum}` === query;
        const promptMatch = (q.prompt || '').toLowerCase().includes(query);
        const passageMatch = (q.passage || '').toLowerCase().includes(query);
        const expMatch = (q.explanation || '').toLowerCase().includes(query);
        const optMatch = (q.options || []).some(o => (o.text || '').toLowerCase().includes(query) || (o.key || '').toLowerCase() === query);
        if (!idMatch && !qNumMatch && !promptMatch && !passageMatch && !expMatch && !optMatch) {
          return false;
        }
      }
      return true;
    });

    state.editorFilteredQuestions = filtered;

    // Update stats bar
    if (el.editorResultsCount) {
      el.editorResultsCount.innerHTML = `Đang tìm thấy <strong>${filtered.length}</strong> / 480 câu hỏi`;
    }
    const totalEdited = Object.keys(state.customOverrides).length;
    if (el.editorEditedCountBadge) {
      el.editorEditedCountBadge.textContent = `${totalEdited} câu đã chỉnh sửa`;
    }

    // Paginate visible
    const visibleQuestions = filtered.slice(0, state.editorVisibleLimit);

    if (el.editorPaginationBar) {
      el.editorPaginationBar.style.display = (visibleQuestions.length < filtered.length) ? 'flex' : 'none';
    }

    if (!appendOnly) {
      el.editorQuestionsContainer.innerHTML = '';
    }

    if (visibleQuestions.length === 0) {
      el.editorQuestionsContainer.innerHTML = `
        <div style="text-align:center; padding: 48px 20px; color: var(--text-muted); background: var(--bg-surface); border-radius: var(--radius-md); border: 1px dashed var(--border-color);">
          <div style="font-size:36px; margin-bottom:12px;">🔍</div>
          <h3 style="margin-bottom:8px; color:var(--text-main);">Không tìm thấy câu hỏi phù hợp</h3>
          <p>Thử tìm với từ khóa khác (ví dụ: fireplace, bicycles, expect, shopping, số câu...) hoặc chọn bộ lọc "Tất cả".</p>
        </div>
      `;
      return;
    }

    // Render cards
    const startIndex = appendOnly ? el.editorQuestionsContainer.children.length : 0;
    const cardsToRender = visibleQuestions.slice(startIndex);

    cardsToRender.forEach(q => {
      const card = createQuestionEditCard(q);
      el.editorQuestionsContainer.appendChild(card);
    });
  }

  function createQuestionEditCard(q) {
    const card = document.createElement('div');
    card.className = 'question-edit-card';
    card.dataset.qid = q.id;
    card.dataset.skill = q.skill;

    const isEdited = !!state.customOverrides[q.id];
    if (isEdited) card.classList.add('is-edited');

    const currentCorrect = (state.customOverrides[q.id] && state.customOverrides[q.id].correctAnswer)
      ? state.customOverrides[q.id].correctAnswer
      : q.correctAnswer;

    const currentExp = (state.customOverrides[q.id] && state.customOverrides[q.id].explanation !== undefined)
      ? state.customOverrides[q.id].explanation
      : (q.explanation || '');

    const expText = currentExp.replace(/<br\s*[\/]?>/gi, '\n');

    const skillLabel = q.skill === 'listening' ? '🎧 Listening' : '📖 Reading B1';
    const skillClass = q.skill === 'reading' ? 'reading' : '';

    let audioButtonHtml = '';
    if (q.audio) {
      audioButtonHtml = `<button class="btn-mini-audio" data-audio="${q.audio}">🔊 Nghe</button>`;
    }

    let imageHtml = '';
    if (q.image) {
      imageHtml = `<div class="q-edit-image-wrap"><img src="${q.image}" alt="Question Image" loading="lazy"></div>`;
    }

    let passageHtml = '';
    if (q.passage && q.passage.trim()) {
      passageHtml = `<div class="q-edit-passage-preview"><strong>Đoạn văn đọc hiểu:</strong><br>${q.passage}</div>`;
    }

    const optionsHtml = (q.options || []).map(opt => {
      const isSelected = (opt.key === currentCorrect);
      return `
        <div class="q-edit-option-item ${isSelected ? 'selected-correct' : ''}" data-key="${opt.key}">
          <span class="q-edit-opt-key">${opt.key}</span>
          <span class="q-edit-opt-text">${escapeHtml(opt.text || '')}</span>
          <span class="q-edit-correct-tag">✓ ĐÁP ÁN ĐÚNG</span>
        </div>
      `;
    }).join('');

    card.innerHTML = `
      <div class="q-edit-header">
        <div class="q-edit-badges">
          <span class="q-badge-skill ${skillClass}">${skillLabel}</span>
          <span class="q-badge-test">Test ${q.test} • Part ${q.part} • Câu ${q.questionNum}</span>
          <span class="q-badge-test" style="font-family:monospace; font-size:11px;">#${q.id}</span>
          ${isEdited ? '<span class="q-badge-edited">✨ ĐÃ CHỈNH SỬA</span>' : ''}
        </div>
        <div class="q-edit-header-actions">
          ${audioButtonHtml}
        </div>
      </div>

      <div class="q-edit-body">
        ${imageHtml}
        ${passageHtml}
        <div class="q-edit-prompt">${escapeHtml(q.prompt || '')}</div>
        
        <div style="font-size:12.5px; font-weight:700; color:var(--text-muted); margin-top:4px;">
          CHỌN ĐÁP ÁN ĐÚNG (Click vào đáp án bên dưới để đổi sang đáp án đúng):
        </div>
        <div class="q-edit-options-list">
          ${optionsHtml}
        </div>

        <div class="q-edit-explanation-wrap">
          <label class="q-edit-explanation-label">Lời giải thích & dịch nghĩa câu hỏi:</label>
          <textarea class="q-edit-explanation-textarea" rows="2" placeholder="Nhập lời giải thích cho câu hỏi này...">${escapeHtml(expText)}</textarea>
        </div>
      </div>

      <div class="q-edit-footer">
        <span class="q-edit-feedback-msg" id="feedback_${q.id}">✓ Đã lưu thành công!</span>
        <div class="q-edit-footer-btns">
          ${isEdited ? `<button class="btn btn-outline btn-sm btn-reset-q" title="Xóa thay đổi và dùng lại đáp án ban đầu">🔄 Khôi Phục Gốc</button>` : ''}
          <button class="btn btn-primary btn-sm btn-save-q">💾 Lưu Thay Đổi</button>
        </div>
      </div>
    `;

    // Event listeners
    let stagedCorrectAns = currentCorrect;
    const optionItems = card.querySelectorAll('.q-edit-option-item');
    optionItems.forEach(item => {
      item.addEventListener('click', () => {
        optionItems.forEach(i => i.classList.remove('selected-correct'));
        item.classList.add('selected-correct');
        stagedCorrectAns = item.dataset.key;
      });
    });

    const btnAudio = card.querySelector('.btn-mini-audio');
    if (btnAudio) {
      btnAudio.addEventListener('click', () => {
        playEditorAudio(q.audio, btnAudio);
      });
    }

    const btnSave = card.querySelector('.btn-save-q');
    const textareaExp = card.querySelector('.q-edit-explanation-textarea');
    btnSave.addEventListener('click', () => {
      const expVal = textareaExp.value.trim().replace(/\n/g, '<br>');
      saveQuestionEdit(q.id, q.skill, stagedCorrectAns, expVal, card);
    });

    const btnReset = card.querySelector('.btn-reset-q');
    if (btnReset) {
      btnReset.addEventListener('click', () => {
        resetQuestionOverride(q.id, card);
      });
    }

    return card;
  }

  function saveQuestionEdit(qid, skill, newAnswer, newExp, cardEl) {
    if (!newAnswer) {
      alert('Vui lòng chọn 1 đáp án đúng (A, B, C, D)');
      return;
    }

    state.customOverrides[qid] = {
      correctAnswer: newAnswer,
      explanation: newExp,
      skill: skill,
      updatedAt: new Date().toISOString()
    };

    try {
      localStorage.setItem('toeic_custom_overrides', JSON.stringify(state.customOverrides));
    } catch (e) {
      console.warn('Cannot write to localStorage', e);
    }

    applyAllOverrides();

    if (cardEl) {
      cardEl.classList.add('is-edited');
      const badgeContainer = cardEl.querySelector('.q-edit-badges');
      if (badgeContainer && !badgeContainer.querySelector('.q-badge-edited')) {
        const editedBadge = document.createElement('span');
        editedBadge.className = 'q-badge-edited';
        editedBadge.textContent = '✨ ĐÃ CHỈNH SỬA';
        badgeContainer.appendChild(editedBadge);
      }
      const feedback = cardEl.querySelector('.q-edit-feedback-msg');
      if (feedback) {
        feedback.classList.add('show');
        setTimeout(() => feedback.classList.remove('show'), 2500);
      }
      const footerBtns = cardEl.querySelector('.q-edit-footer-btns');
      if (footerBtns && !footerBtns.querySelector('.btn-reset-q')) {
        const btnReset = document.createElement('button');
        btnReset.className = 'btn btn-outline btn-sm btn-reset-q';
        btnReset.title = 'Xóa thay đổi và dùng lại đáp án ban đầu';
        btnReset.textContent = '🔄 Khôi Phục Gốc';
        btnReset.addEventListener('click', () => resetQuestionOverride(qid, cardEl));
        footerBtns.insertBefore(btnReset, footerBtns.firstChild);
      }
    }

    const totalEdited = Object.keys(state.customOverrides).length;
    if (el.editorEditedCountBadge) {
      el.editorEditedCountBadge.textContent = `${totalEdited} câu đã chỉnh sửa`;
    }

    showToast(`✓ Đã lưu đáp án câu [${qid}] thành (${newAnswer})!`);

    fetch('/api/save_question', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: qid,
        skill: skill,
        correctAnswer: newAnswer,
        explanation: newExp
      })
    }).then(res => res.json()).then(data => {
      if (data && data.success) {
        showToast(`✓ File dữ liệu (${skill === 'listening' ? 'toeic_app_data.js' : 'toeic_reading_data.js'}) đã được cập nhật vĩnh viễn!`);
      }
    }).catch(() => {
      // Offline mode or file:/// - localStorage persists changes
    });
  }

  function resetQuestionOverride(qid, cardEl) {
    if (!confirm(`Khôi phục câu hỏi [${qid}] về đáp án gốc ban đầu?`)) return;

    delete state.customOverrides[qid];
    localStorage.setItem('toeic_custom_overrides', JSON.stringify(state.customOverrides));

    showToast(`✓ Đã khôi phục câu [${qid}] về đáp án gốc!`);
    renderEditorQuestions();
  }

  function exportCustomData() {
    const overrides = state.customOverrides;
    const count = Object.keys(overrides).length;
    if (count === 0) {
      alert('Hiện tại bạn chưa chỉnh sửa câu hỏi nào!');
      return;
    }
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(overrides, null, 2));
    const dlAnchorElem = document.createElement('a');
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", `toeic_custom_overrides_${new Date().toISOString().slice(0, 10)}.json`);
    dlAnchorElem.click();
    showToast(`✓ Đã xuất file sao lưu ${count} câu đã chỉnh sửa!`);
  }

  function resetAllOverrides() {
    const count = Object.keys(state.customOverrides).length;
    if (count === 0) {
      alert('Hiện tại không có câu hỏi nào được chỉnh sửa.');
      return;
    }
    if (confirm(`Bạn có chắc chắn muốn xóa TOÀN BỘ ${count} câu đã chỉnh sửa và khôi phục tất cả về đáp án gốc ban đầu?`)) {
      state.customOverrides = {};
      localStorage.removeItem('toeic_custom_overrides');
      alert('Đã xóa tất cả chỉnh sửa! Trang sẽ tự động tải lại để khôi phục dữ liệu gốc.');
      window.location.reload();
    }
  }

  function showToast(msg) {
    let toast = document.getElementById('appGlobalToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'appGlobalToast';
      toast.className = 'app-toast-message';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.display = 'flex';
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => {
      toast.style.display = 'none';
    }, 3500);
  }

  // =========================================================================
  // UTILITIES
  // =========================================================================
  function debounce(fn, delay) {
    let timer = null;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatMinutesSeconds(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }

  function formatTime(sec) {
    if (isNaN(sec)) return '00:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }


  // =========================================================================
  // SPEAKING MODULE LOGIC (ENGLISH SPEAKING TOPICS B1)
  // =========================================================================

  function openSpeakingMode() {
    stopAudio();
    stopTransAudio();
    stopEditorAudio();
    stopAllSpeakingAudio();
    showScreen('speaking');
    initSpeakingModule();
  }

  function stopAllSpeakingAudio() {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    if (state.speakingIsRecording) {
      stopP1Recording();
      stopP2Recording();
    }
    if (state.speakingExamInterval) {
      clearInterval(state.speakingExamInterval);
      state.speakingExamInterval = null;
    }
    if (el.p1UserAudioPlayer) {
      el.p1UserAudioPlayer.pause();
    }
    if (el.p2UserAudioPlayer) {
      el.p2UserAudioPlayer.pause();
    }
    if (el.speakingStatusBadge) {
      el.speakingStatusBadge.className = 'speaking-status-badge';
      el.speakingStatusBadge.textContent = '🎙️ Sẵn sàng luyện nói';
    }
  }

  function speakEnglish(text, customRate) {
    if (!('speechSynthesis' in window)) {
      showToast('⚠️ Trình duyệt của bạn không hỗ trợ phát âm Web Speech API.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = customRate || state.speakingStudySpeed || 0.95;
    utterance.pitch = 1.0;

    const voices = window.speechSynthesis.getVoices();
    const enVoice = voices.find(v => v.lang === 'en-US' || v.lang === 'en_US') ||
                    voices.find(v => v.lang && v.lang.startsWith('en'));
    if (enVoice) {
      utterance.voice = enVoice;
    }

    if (el.speakingStatusBadge) {
      el.speakingStatusBadge.className = 'speaking-status-badge';
      el.speakingStatusBadge.textContent = '🔊 Đang phát âm bài mẫu...';
    }

    utterance.onend = () => {
      if (el.speakingStatusBadge) {
        el.speakingStatusBadge.className = 'speaking-status-badge';
        el.speakingStatusBadge.textContent = '🎙️ Sẵn sàng luyện nói';
      }
    };

    window.speechSynthesis.speak(utterance);
  }

  function playExamBeep(isHigh) {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = 'sine';

      if (isHigh) {
        osc.frequency.setValueAtTime(880, ctx.currentTime);
        gain.gain.setValueAtTime(0.25, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
        osc.start();
        osc.stop(ctx.currentTime + 0.5);
      } else {
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        gain.gain.setValueAtTime(0.18, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
        osc.start();
        osc.stop(ctx.currentTime + 0.3);
      }
    } catch (e) {
      // AudioContext unavailable
    }
  }

let speakingInitialized = false;

  function initSpeakingModule() {
    if (!window.TOEIC_SPEAKING_DATA) {
      console.warn("TOEIC_SPEAKING_DATA not loaded yet.");
      return;
    }

    if (!speakingInitialized) {
      bindSpeakingEvents();
      speakingInitialized = true;
    }

    renderP1Topics();
    loadP1Question();
    renderP2Topics();
    loadP2Topic();

    // Default to study subtab
    switchSpeakingSubtab(state.speakingSubtab || 'study');
  }

  function bindSpeakingEvents() {
    // Subtabs
    if (el.btnSpeakingSubtabStudy) {
      el.btnSpeakingSubtabStudy.addEventListener('click', () => switchSpeakingSubtab('study'));
    }
    el.btnSpeakingSubtabPart1.addEventListener('click', () => switchSpeakingSubtab('part1'));
    el.btnSpeakingSubtabPart2.addEventListener('click', () => switchSpeakingSubtab('part2'));
    el.btnSpeakingSubtabExam.addEventListener('click', () => switchSpeakingSubtab('exam'));

    // Speaking Study Filter Pills
    if (el.speakingStudyFilterPills) {
      el.speakingStudyFilterPills.addEventListener('click', (e) => {
        const pill = e.target.closest('.study-pill');
        if (!pill) return;
        el.speakingStudyFilterPills.querySelectorAll('.study-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.speakingStudyFilter = pill.dataset.filter || 'all';
        renderSpeakingStudyCards();
      });
    }

    // Speaking Study Search
    if (el.speakingStudySearchInput) {
      el.speakingStudySearchInput.addEventListener('input', () => {
        state.speakingStudySearch = el.speakingStudySearchInput.value.trim().toLowerCase();
        renderSpeakingStudyCards();
      });
    }

    if (el.btnClearStudySearch) {
      el.btnClearStudySearch.addEventListener('click', () => {
        if (el.speakingStudySearchInput) el.speakingStudySearchInput.value = '';
        state.speakingStudySearch = '';
        renderSpeakingStudyCards();
      });
    }

    // Speaking Study Speed
    if (el.speakingStudySpeedSelect) {
      el.speakingStudySpeedSelect.addEventListener('change', () => {
        state.speakingStudySpeed = parseFloat(el.speakingStudySpeedSelect.value) || 0.95;
      });
    }

    // Speaking Study Toggle Vi Translation
    if (el.btnToggleStudyViTranslation) {
      el.btnToggleStudyViTranslation.addEventListener('click', () => {
        state.speakingStudyShowVi = !state.speakingStudyShowVi;
        if (el.speakingStudyCardsContainer) {
          el.speakingStudyCardsContainer.classList.toggle('hide-study-vi', !state.speakingStudyShowVi);
        }
        el.btnToggleStudyViTranslation.textContent = state.speakingStudyShowVi 
          ? '👁️ Ẩn Lời Dịch Tiếng Việt' 
          : '🌐 Hiện Lời Dịch Tiếng Việt';
      });
    }

    // Speaking Study Cards Event Delegation
    if (el.speakingStudyCardsContainer) {
      el.speakingStudyCardsContainer.addEventListener('click', (e) => {
        // Listen audio
        const btnListen = e.target.closest('.btn-study-listen');
        if (btnListen) {
          const text = btnListen.dataset.speak;
          if (text) speakEnglish(text, state.speakingStudySpeed);
          return;
        }

        // Copy text
        const btnCopy = e.target.closest('.btn-study-copy');
        if (btnCopy) {
          const text = btnCopy.dataset.copy;
          if (text) {
            navigator.clipboard.writeText(text).then(() => {
              const origHtml = btnCopy.innerHTML;
              btnCopy.innerHTML = '✅ Đã chép!';
              setTimeout(() => { btnCopy.innerHTML = origHtml; }, 1800);
              showToast('✅ Đã sao chép nội dung vào bộ nhớ tạm!');
            }).catch(() => {
              showToast('⚠️ Không thể tự động sao chép. Hãy bôi đen và copy thủ công.');
            });
          }
          return;
        }

        // Click vocab chip to hear
        const chip = e.target.closest('.study-vocab-chip');
        if (chip) {
          const word = chip.dataset.word;
          if (word) speakEnglish(word, 0.9);
          return;
        }

        // Jump to Part 1 practice
        const btnJumpP1 = e.target.closest('[data-jump-p1-topic]');
        if (btnJumpP1) {
          const topicId = btnJumpP1.dataset.jumpP1Topic;
          const qIndex = parseInt(btnJumpP1.dataset.jumpP1Q, 10) || 0;
          state.speakingP1TopicId = topicId;
          state.speakingP1QIndex = qIndex;
          switchSpeakingSubtab('part1');
          renderP1Topics();
          loadP1Question();
          if (el.viewSpeakingPart1) {
            window.scrollTo({ top: el.viewSpeakingPart1.offsetTop - 80, behavior: 'smooth' });
          }
          showToast('🎯 Đã vào phòng luyện nói Part 1! Nhấn Micro để thu âm trả lời.');
          return;
        }

        // Jump to Part 2 practice
        const btnJumpP2 = e.target.closest('[data-jump-p2-index]');
        if (btnJumpP2) {
          const p2Idx = parseInt(btnJumpP2.dataset.jumpP2Index, 10) || 0;
          state.speakingP2TopicIndex = p2Idx;
          switchSpeakingSubtab('part2');
          renderP2Topics();
          loadP2Topic();
          if (el.viewSpeakingPart2) {
            window.scrollTo({ top: el.viewSpeakingPart2.offsetTop - 80, behavior: 'smooth' });
          }
          showToast('🎯 Đã vào phòng luyện nói Part 2! Nhấn Micro để thu âm bài nói.');
          return;
        }
      });
    }

    // Stop audio button
    if (el.btnSpeakingStopAllAudio) {
      el.btnSpeakingStopAllAudio.addEventListener('click', stopAllSpeakingAudio);
    }

    // Part 1 Listen Question
    el.btnP1ListenQuestion.addEventListener('click', () => {
      const q = getCurrentP1Question();
      if (q) speakEnglish(q.question);
    });

    // Part 1 Toggle Record
    el.btnP1RecordToggle.addEventListener('click', toggleP1Recording);

    // Part 1 Toggle Sample
    el.btnToggleP1Sample.addEventListener('click', () => {
      state.speakingShowSampleP1 = !state.speakingShowSampleP1;
      el.p1SampleBox.style.display = state.speakingShowSampleP1 ? 'flex' : 'none';
      el.btnToggleP1Sample.textContent = state.speakingShowSampleP1 
        ? '🙈 Ẩn Câu Trả Lời Mẫu' 
        : '👁️ Hiện Câu Trả Lời Mẫu & Lời Dịch';
    });

    // Part 1 Listen Sample
    el.btnP1ListenSample.addEventListener('click', () => {
      const q = getCurrentP1Question();
      if (q) speakEnglish(q.sampleAnswer);
    });

    // Part 1 Prev / Next
    el.btnP1PrevQ.addEventListener('click', () => {
      const topic = getCurrentP1Topic();
      if (!topic) return;
      if (state.speakingP1QIndex > 0) {
        state.speakingP1QIndex--;
        loadP1Question();
      }
    });

    el.btnP1NextQ.addEventListener('click', () => {
      const topic = getCurrentP1Topic();
      if (!topic) return;
      if (state.speakingP1QIndex < topic.questions.length - 1) {
        state.speakingP1QIndex++;
        loadP1Question();
      }
    });

    // Part 2 Listen Topic
    el.btnP2ListenTopic.addEventListener('click', () => {
      const topic = getCurrentP2Topic();
      if (topic) speakEnglish(topic.title);
    });

    // Part 2 Toggle Record
    el.btnP2RecordToggle.addEventListener('click', toggleP2Recording);

    // Part 2 Toggle Sample
    el.btnToggleP2Sample.addEventListener('click', () => {
      state.speakingShowSampleP2 = !state.speakingShowSampleP2;
      el.p2SampleBox.style.display = state.speakingShowSampleP2 ? 'flex' : 'none';
      el.btnToggleP2Sample.textContent = state.speakingShowSampleP2 
        ? '🙈 Ẩn Bài Nói Mẫu' 
        : '👁️ Xem Bài Nói Mẫu Hoàn Chỉnh (Full Speech) & Dịch Nghĩa';
    });

    // Part 2 Listen Full Speech
    el.btnP2ListenFullSpeech.addEventListener('click', () => {
      const topic = getCurrentP2Topic();
      if (topic) speakEnglish(topic.fullSpeechEn);
    });

    // Part 2 Prev / Next
    el.btnP2PrevTopic.addEventListener('click', () => {
      if (state.speakingP2TopicIndex > 0) {
        state.speakingP2TopicIndex--;
        loadP2Topic();
      }
    });

    el.btnP2NextTopic.addEventListener('click', () => {
      const total = window.TOEIC_SPEAKING_DATA.part2_topics.length;
      if (state.speakingP2TopicIndex < total - 1) {
        state.speakingP2TopicIndex++;
        loadP2Topic();
      }
    });

    // Exam Type Selection
    [el.examTypeP1, el.examTypeP2, el.examTypeFull].forEach(card => {
      if (!card) return;
      card.addEventListener('click', () => {
        [el.examTypeP1, el.examTypeP2, el.examTypeFull].forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        state.speakingExamType = card.dataset.examType;
      });
    });

    // Start Exam
    el.btnStartSpeakingExam.addEventListener('click', startSpeakingExam);
    el.btnQuitSpeakingExam.addEventListener('click', quitSpeakingExam);
    el.btnSkipExamPrep.addEventListener('click', skipExamPrep);
    el.btnNextExamItem.addEventListener('click', finishExamStep);
    el.btnRetakeSpeakingExam.addEventListener('click', startSpeakingExam);
    el.btnBackToSpeakingPractice.addEventListener('click', () => switchSpeakingSubtab('part1'));
  }

  function switchSpeakingSubtab(subtab) {
    state.speakingSubtab = subtab;
    stopAllSpeakingAudio();

    if (el.btnSpeakingSubtabStudy) el.btnSpeakingSubtabStudy.classList.toggle('active', subtab === 'study');
    el.btnSpeakingSubtabPart1.classList.toggle('active', subtab === 'part1');
    el.btnSpeakingSubtabPart2.classList.toggle('active', subtab === 'part2');
    el.btnSpeakingSubtabExam.classList.toggle('active', subtab === 'exam');

    if (el.viewSpeakingStudy) el.viewSpeakingStudy.style.display = (subtab === 'study') ? 'block' : 'none';
    el.viewSpeakingPart1.style.display = (subtab === 'part1') ? 'block' : 'none';
    el.viewSpeakingPart2.style.display = (subtab === 'part2') ? 'block' : 'none';
    el.viewSpeakingExam.style.display = (subtab === 'exam') ? 'block' : 'none';

    if (subtab === 'study') {
      renderSpeakingStudyCards();
    } else if (subtab === 'exam') {
      el.speakingExamSetup.style.display = 'flex';
      el.speakingExamActive.style.display = 'none';
      el.speakingExamResult.style.display = 'none';
    }
  }

  function renderSpeakingStudyCards() {
    if (!el.speakingStudyCardsContainer || !window.TOEIC_SPEAKING_DATA) return;

    const filter = state.speakingStudyFilter || 'all';
    const search = (state.speakingStudySearch || '').toLowerCase().trim();

    let cardsHtml = '';
    let matchCount = 0;

    // 1. Part 1 questions
    if (filter === 'all' || filter === 'tech' || filter === 'holiday' || filter === 'travel' || filter === 'shopping') {
      window.TOEIC_SPEAKING_DATA.part1_topics.forEach(topic => {
        if (filter !== 'all' && topic.id !== filter) return;

        topic.questions.forEach((q, qIndex) => {
          if (search) {
            const haystack = [
              topic.name, topic.nameVi, q.question, q.questionVi, q.sampleAnswer, q.sampleVi,
              ...(q.vocabulary || []).map(v => `${v.word} ${v.meaning}`),
              ...(q.templates || [])
            ].join(' ').toLowerCase();

            if (!haystack.includes(search)) return;
          }

          matchCount++;

          const vocabHtml = (q.vocabulary && q.vocabulary.length > 0)
            ? `<div class="study-helper-box">
                <div class="study-helper-title">✨ Từ vựng ghi điểm (Click để nghe)</div>
                <div class="study-vocab-chips">
                  ${q.vocabulary.map(v => `
                    <button class="study-vocab-chip" type="button" data-word="${escapeHtml(v.word)}" title="Bấm để nghe phát âm: ${escapeHtml(v.word)}">
                      <strong>${escapeHtml(v.word)}</strong> <span style="font-size:11px;opacity:0.8;">(${escapeHtml(v.type || '')})</span>: <span class="meaning">${escapeHtml(v.meaning || '')}</span>
                    </button>
                  `).join('')}
                </div>
              </div>`
            : '';

          const templatesHtml = (q.templates && q.templates.length > 0)
            ? `<div class="study-helper-box">
                <div class="study-helper-title">🎯 Cấu trúc câu gợi ý (Templates)</div>
                <ul class="study-templates-list">
                  ${q.templates.map(t => `<li>${escapeHtml(t)}</li>`).join('')}
                </ul>
              </div>`
            : '';

          cardsHtml += `
            <div class="speaking-study-card">
              <div class="study-card-top">
                <div class="study-card-badges">
                  <span class="study-badge-tag">${topic.icon || '📌'} ${escapeHtml(topic.name)} (${escapeHtml(topic.nameVi)})</span>
                  <span class="study-badge-part">Part 1 • Câu ${q.num}/6</span>
                </div>
              </div>

              <div class="study-q-section">
                <div class="study-q-en">
                  ${escapeHtml(q.question)}
                  <button class="btn-study-listen btn-study-listen-q" type="button" data-speak="${escapeHtml(q.question)}" title="Nghe câu hỏi">🔊 Nghe câu hỏi</button>
                </div>
                <div class="study-q-vi">${escapeHtml(q.questionVi)}</div>
              </div>

              <div class="study-a-section">
                <div class="study-a-header">
                  <span>💡 Câu Trả Lời Mẫu B1 Chuẩn</span>
                  <div class="study-a-actions">
                    <button class="btn-study-listen" type="button" data-speak="${escapeHtml(q.sampleAnswer)}" title="Nghe câu trả lời mẫu">🔊 Nghe mẫu</button>
                    <button class="btn-study-copy" type="button" data-copy="${escapeHtml(q.sampleAnswer)}" title="Sao chép câu trả lời">📋 Sao chép</button>
                  </div>
                </div>
                <div class="study-a-en">${escapeHtml(q.sampleAnswer)}</div>
                <div class="study-a-vi">${escapeHtml(q.sampleVi)}</div>
              </div>

              ${(vocabHtml || templatesHtml) ? `<div class="study-helpers-row">${vocabHtml}${templatesHtml}</div>` : ''}

              <div class="study-card-footer">
                <button class="btn-jump-practice" type="button" data-jump-p1-topic="${topic.id}" data-jump-p1-q="${qIndex}">
                  🎙️ Vào Luyện Nói & Thu Âm Câu Này (Part 1)
                </button>
              </div>
            </div>
          `;
        });
      });
    }

    // 2. Part 2 topics
    if (filter === 'all' || filter === 'part2') {
      window.TOEIC_SPEAKING_DATA.part2_topics.forEach((topic, p2Index) => {
        if (search) {
          const haystack = [
            topic.title, topic.titleVi, topic.fullSpeechEn, topic.fullSpeechVi,
            ...(topic.cues || []).map(c => `${c.cue} ${c.cueVi} ${c.answer} ${c.answerVi}`),
            ...(topic.vocabulary || []).map(v => `${v.word} ${v.meaning}`),
            ...(topic.transitionPhrases || [])
          ].join(' ').toLowerCase();

          if (!haystack.includes(search)) return;
        }

        matchCount++;

        const cuesSummaryHtml = (topic.cues && topic.cues.length > 0)
          ? `<div style="background:var(--bg-surface-elevated); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:10px 14px; margin-bottom:12px;">
              <div style="font-size:12px; font-weight:700; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.04em; margin-bottom:6px;">📋 4 Gợi ý trả lời (Cues dàn ý):</div>
              <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:8px;">
                ${topic.cues.map((c, ci) => `
                  <div class="study-cue-row" style="font-size:12.5px; background:var(--bg-surface); border:1px solid var(--border-color); border-radius:6px; padding:6px 10px;">
                    <div style="font-weight:700; color:var(--primary); margin-bottom:2px;">${ci+1}. ${escapeHtml(c.cue)}:</div>
                    <div style="color:var(--text-main); font-weight:500;">${escapeHtml(c.answer)}</div>
                    <div class="cue-vi" style="color:var(--text-muted); font-size:12px; margin-top:2px;">${escapeHtml(c.answerVi)}</div>
                  </div>
                `).join('')}
              </div>
            </div>`
          : '';

        const vocabHtml = (topic.vocabulary && topic.vocabulary.length > 0)
          ? `<div class="study-helper-box">
              <div class="study-helper-title">✨ Từ vựng ghi điểm (Click để nghe)</div>
              <div class="study-vocab-chips">
                ${topic.vocabulary.map(v => `
                  <button class="study-vocab-chip" type="button" data-word="${escapeHtml(v.word)}" title="Bấm để nghe phát âm: ${escapeHtml(v.word)}">
                    <strong>${escapeHtml(v.word)}</strong> <span style="font-size:11px;opacity:0.8;">(${escapeHtml(v.type || '')})</span>: <span class="meaning">${escapeHtml(v.meaning || '')}</span>
                  </button>
                `).join('')}
              </div>
            </div>`
          : '';

        const transitionsHtml = (topic.transitionPhrases && topic.transitionPhrases.length > 0)
          ? `<div class="study-helper-box">
              <div class="study-helper-title">🔗 Từ nối liên kết câu (Transition Phrases)</div>
              <ul class="study-templates-list">
                ${topic.transitionPhrases.map(t => `<li>${escapeHtml(t)}</li>`).join('')}
              </ul>
            </div>`
          : '';

        cardsHtml += `
          <div class="speaking-study-card">
            <div class="study-card-top">
              <div class="study-card-badges">
                <span class="study-badge-tag">${topic.icon || '🗣️'} Part 2: Độc Thoại Chủ Đề ${topic.topicNumber || ''}</span>
                <span class="study-badge-part" style="background:rgba(234, 88, 12, 0.1); color:#ea580c; border:1px solid rgba(234, 88, 12, 0.2);">⏱️ ${escapeHtml(topic.targetTime || '1.5 - 2 phút')}</span>
              </div>
            </div>

            <div class="study-q-section">
              <div class="study-q-en" style="font-size:18px;">
                ${escapeHtml(topic.title)}
                <button class="btn-study-listen btn-study-listen-q" type="button" data-speak="${escapeHtml(topic.title)}" title="Nghe chủ đề">🔊 Nghe chủ đề</button>
              </div>
              <div class="study-q-vi" style="font-size:15px;">${escapeHtml(topic.titleVi)}</div>
            </div>

            ${cuesSummaryHtml}

            <div class="study-a-section" style="border-left-color: #ea580c;">
              <div class="study-a-header">
                <span style="color:#ea580c;">🌟 Bài Nói Mẫu Hoàn Chỉnh (${topic.wordCount || 100} từ)</span>
                <div class="study-a-actions">
                  <button class="btn-study-listen" type="button" data-speak="${escapeHtml(topic.fullSpeechEn)}" title="Nghe phát âm toàn bài độc thoại">🔊 Nghe toàn bài</button>
                  <button class="btn-study-copy" type="button" data-copy="${escapeHtml(topic.fullSpeechEn)}" title="Sao chép toàn bài">📋 Sao chép</button>
                </div>
              </div>
              <div class="study-a-en" style="line-height:1.65;">${escapeHtml(topic.fullSpeechEn)}</div>
              <div class="study-a-vi" style="line-height:1.6; margin-top:8px;">${escapeHtml(topic.fullSpeechVi)}</div>
            </div>

            ${(vocabHtml || transitionsHtml) ? `<div class="study-helpers-row">${vocabHtml}${transitionsHtml}</div>` : ''}

            <div class="study-card-footer">
              <button class="btn-jump-practice" type="button" data-jump-p2-index="${p2Index}">
                🎙️ Vào Luyện Độc Thoại & Thu Âm Chủ Đề Này (Part 2)
              </button>
            </div>
          </div>
        `;
      });
    }

    if (matchCount === 0) {
      el.speakingStudyCardsContainer.innerHTML = `
        <div style="text-align:center; padding:48px 20px; color:var(--text-muted); grid-column:1/-1;">
          <div style="font-size:42px; margin-bottom:12px;">🔍</div>
          <h4 style="color:var(--text-main); margin-bottom:6px;">Không tìm thấy nội dung phù hợp</h4>
          <p>Không có câu hỏi hoặc từ vựng nào khớp với từ khóa "<strong>${escapeHtml(search)}</strong>". Hãy thử từ khóa khác!</p>
        </div>
      `;
      return;
    }

    el.speakingStudyCardsContainer.innerHTML = cardsHtml;
    el.speakingStudyCardsContainer.classList.toggle('hide-study-vi', !state.speakingStudyShowVi);
  }

  // --- PART 1 LOGIC ---

  function getCurrentP1Topic() {
    return window.TOEIC_SPEAKING_DATA.part1_topics.find(t => t.id === state.speakingP1TopicId) ||
           window.TOEIC_SPEAKING_DATA.part1_topics[0];
  }

  function getCurrentP1Question() {
    const topic = getCurrentP1Topic();
    if (!topic || !topic.questions) return null;
    return topic.questions[state.speakingP1QIndex] || topic.questions[0];
  }

  function renderP1Topics() {
    el.speakingP1TopicSelector.innerHTML = '';
    window.TOEIC_SPEAKING_DATA.part1_topics.forEach(topic => {
      const pill = document.createElement('button');
      pill.className = `speaking-topic-pill ${topic.id === state.speakingP1TopicId ? 'active' : ''}`;
      pill.innerHTML = `<span>${topic.icon}</span> <span>${topic.nameVi} (${topic.questions.length}c)</span>`;
      pill.addEventListener('click', () => {
        state.speakingP1TopicId = topic.id;
        state.speakingP1QIndex = 0;
        renderP1Topics();
        loadP1Question();
      });
      el.speakingP1TopicSelector.appendChild(pill);
    });
  }

  function loadP1Question() {
    stopAllSpeakingAudio();
    const topic = getCurrentP1Topic();
    const q = getCurrentP1Question();
    if (!topic || !q) return;

    // Header info
    el.speakingP1TopicBadge.textContent = `${topic.icon} ${topic.name} (${topic.nameVi})`;
    el.speakingP1QNumBadge.textContent = `Câu ${state.speakingP1QIndex + 1} / ${topic.questions.length}`;

    // Question
    el.speakingP1QuestionText.textContent = q.question;
    el.speakingP1QuestionVi.textContent = q.questionVi;

    // Reset recording area
    el.p1TranscriptText.textContent = 'Nhấn nút "Bắt Đầu Nói" và trả lời câu hỏi bằng tiếng Anh...';
    el.p1TranscriptWordCount.textContent = '0 từ';
    el.p1UserAudioWrap.style.display = 'none';

    // Sample box reset
    state.speakingShowSampleP1 = false;
    el.p1SampleBox.style.display = 'none';
    el.btnToggleP1Sample.textContent = '👁️ Hiện Câu Trả Lời Mẫu & Lời Dịch';
    el.p1SampleEn.textContent = `"${q.sampleAnswer}"`;
    el.p1SampleVi.textContent = q.sampleVi;

    // Vocabulary
    el.p1VocabList.innerHTML = q.vocabulary.map(v => 
      `<li><strong>${v.word}</strong> <span style="color:var(--text-muted); font-size:12px;">(${v.type})</span>: ${v.meaning}</li>`
    ).join('');

    // Templates
    el.p1TemplateList.innerHTML = q.templates.map(t => 
      `<li><span style="color:var(--primary);">➤</span> <em>"${t}"</em></li>`
    ).join('');

    // Pagination pills
    renderP1QPills(topic);

    // Prev / Next button states
    el.btnP1PrevQ.disabled = (state.speakingP1QIndex === 0);
    el.btnP1NextQ.disabled = (state.speakingP1QIndex === topic.questions.length - 1);
  }

  function renderP1QPills(topic) {
    el.p1QPillsContainer.innerHTML = '';
    topic.questions.forEach((_, idx) => {
      const btn = document.createElement('button');
      btn.className = `speaking-q-pill ${idx === state.speakingP1QIndex ? 'active' : ''}`;
      btn.textContent = idx + 1;
      btn.addEventListener('click', () => {
        state.speakingP1QIndex = idx;
        loadP1Question();
      });
      el.p1QPillsContainer.appendChild(btn);
    });
  }

  // --- PART 2 LOGIC ---

  function getCurrentP2Topic() {
    return window.TOEIC_SPEAKING_DATA.part2_topics[state.speakingP2TopicIndex] ||
           window.TOEIC_SPEAKING_DATA.part2_topics[0];
  }

  function renderP2Topics() {
    el.speakingP2TopicSelector.innerHTML = '';
    window.TOEIC_SPEAKING_DATA.part2_topics.forEach((topic, idx) => {
      const pill = document.createElement('button');
      pill.className = `speaking-topic-pill ${idx === state.speakingP2TopicIndex ? 'active' : ''}`;
      pill.innerHTML = `<span>${topic.icon}</span> <span>Đề ${topic.topicNumber}: ${topic.titleVi}</span>`;
      pill.addEventListener('click', () => {
        state.speakingP2TopicIndex = idx;
        renderP2Topics();
        loadP2Topic();
      });
      el.speakingP2TopicSelector.appendChild(pill);
    });
  }

  function loadP2Topic() {
    stopAllSpeakingAudio();
    const topic = getCurrentP2Topic();
    if (!topic) return;

    el.speakingP2TopicBadge.textContent = `${topic.icon} Đề ${topic.topicNumber}`;
    el.speakingP2TimeBadge.textContent = topic.targetTime;

    el.speakingP2TitleEn.textContent = topic.title;
    el.speakingP2TitleVi.textContent = topic.titleVi;

    // Render 4 cues cards
    el.p2CuesGrid.innerHTML = topic.cues.map((c, idx) => `
      <div class="cue-card-item">
        <span class="cue-card-num">Gợi ý ${idx + 1}</span>
        <span class="cue-card-en">${c.cue}</span>
        <span class="cue-card-vi">${c.cueVi}</span>
      </div>
    `).join('');

    // Reset recording area
    el.p2TranscriptText.textContent = 'Nhấn nút "Bắt Đầu Nói Độc Thoại" để luyện nói bài thuyết trình...';
    el.p2TranscriptWordCount.textContent = '0 từ';
    el.p2UserAudioWrap.style.display = 'none';

    // Sample box reset
    state.speakingShowSampleP2 = false;
    el.p2SampleBox.style.display = 'none';
    el.btnToggleP2Sample.textContent = '👁️ Xem Bài Nói Mẫu Hoàn Chỉnh (Full Speech) & Dịch Nghĩa';
    el.p2SpeechEn.textContent = `"${topic.fullSpeechEn}"`;
    el.p2SpeechVi.textContent = topic.fullSpeechVi;

    // Vocab
    el.p2VocabList.innerHTML = topic.vocabulary.map(v => 
      `<li><strong>${v.word}</strong> <span style="color:var(--text-muted); font-size:12px;">(${v.type})</span>: ${v.meaning}</li>`
    ).join('');

    // Transitions
    el.p2TransitionList.innerHTML = topic.transitionPhrases.map(t => 
      `<li><span style="color:#10b981;">➤</span> <em>"${t}"</em></li>`
    ).join('');

    // Nav info & buttons
    const total = window.TOEIC_SPEAKING_DATA.part2_topics.length;
    el.p2NavInfo.textContent = `Chủ đề ${state.speakingP2TopicIndex + 1} / ${total}`;
    el.btnP2PrevTopic.disabled = (state.speakingP2TopicIndex === 0);
    el.btnP2NextTopic.disabled = (state.speakingP2TopicIndex === total - 1);
  }

  // --- RECORDING ENGINE (MediaRecorder & SpeechRecognition) ---

  async function startRecordingSession(transcriptTarget, wordCountTarget, audioPlayer, audioWrap, timerElement, timerText) {
    if (state.speakingIsRecording) return;
    state.speakingIsRecording = true;
    state.speakingRecordSeconds = 0;
    state.speakingAudioChunks = [];

    if (el.speakingStatusBadge) {
      el.speakingStatusBadge.className = 'speaking-status-badge recording';
      el.speakingStatusBadge.textContent = '🔴 Đang lắng nghe & ghi âm...';
    }

    transcriptTarget.textContent = 'Đang nghe bạn nói... (Hãy nói to và rõ ràng)';
    wordCountTarget.textContent = '0 từ';
    audioWrap.style.display = 'none';
    timerElement.style.display = 'flex';
    timerText.textContent = '00:00';

    // Start timer interval
    state.speakingRecordTimerInterval = setInterval(() => {
      state.speakingRecordSeconds++;
      timerText.textContent = formatMinutesSeconds(state.speakingRecordSeconds);
    }, 1000);

    // 1. Microphone recording via MediaRecorder
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      state.speakingMediaRecorder = new MediaRecorder(stream);
      state.speakingMediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          state.speakingAudioChunks.push(e.data);
        }
      };
      state.speakingMediaRecorder.onstop = () => {
        const audioBlob = new Blob(state.speakingAudioChunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayer.src = audioUrl;
        audioWrap.style.display = 'flex';
        stream.getTracks().forEach(track => track.stop());
      };
      state.speakingMediaRecorder.start();
    } catch (err) {
      console.warn("Could not access microphone for audio recording:", err);
    }

    // 2. Speech to Text via Web Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      state.speakingRecognition = new SpeechRecognition();
      state.speakingRecognition.lang = 'en-US';
      state.speakingRecognition.continuous = true;
      state.speakingRecognition.interimResults = true;

      let recognizedText = '';
      state.speakingRecognition.onresult = (event) => {
        let interim = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            recognizedText += event.results[i][0].transcript + ' ';
          } else {
            interim += event.results[i][0].transcript;
          }
        }
        const full = (recognizedText + interim).trim();
        transcriptTarget.textContent = full || 'Đang nghe bạn nói...';
        const words = full ? full.split(/\s+/).filter(Boolean).length : 0;
        wordCountTarget.textContent = `${words} từ`;
      };

      state.speakingRecognition.onerror = (e) => {
        console.warn("Speech recognition error:", e.error);
      };

      state.speakingRecognition.start();
    } else {
      transcriptTarget.textContent = '⚠️ Trình duyệt chưa hỗ trợ Web SpeechRecognition (nhận diện giọng nói), nhưng file ghi âm giọng nói của bạn vẫn đang được thu âm!';
    }
  }

  function stopRecordingSession(timerElement) {
    if (!state.speakingIsRecording) return;
    state.speakingIsRecording = false;

    if (state.speakingRecordTimerInterval) {
      clearInterval(state.speakingRecordTimerInterval);
      state.speakingRecordTimerInterval = null;
    }

    if (timerElement) {
      timerElement.style.display = 'none';
    }

    if (state.speakingMediaRecorder && state.speakingMediaRecorder.state !== 'inactive') {
      state.speakingMediaRecorder.stop();
    }

    if (state.speakingRecognition) {
      try {
        state.speakingRecognition.stop();
      } catch (e) {}
      state.speakingRecognition = null;
    }

    if (el.speakingStatusBadge) {
      el.speakingStatusBadge.className = 'speaking-status-badge';
      el.speakingStatusBadge.textContent = '✅ Đã hoàn tất bản thu';
    }
  }

  function toggleP1Recording() {
    if (!state.speakingIsRecording) {
      el.btnP1RecordToggle.classList.add('recording');
      el.p1RecordBtnText.textContent = '⏹️ Dừng Nói';
      startRecordingSession(
        el.p1TranscriptText,
        el.p1TranscriptWordCount,
        el.p1UserAudioPlayer,
        el.p1UserAudioWrap,
        el.p1RecordTimer,
        el.p1RecordTimerText
      );
    } else {
      stopP1Recording();
    }
  }

  function stopP1Recording() {
    el.btnP1RecordToggle.classList.remove('recording');
    el.p1RecordBtnText.textContent = '🎤 Bắt Đầu Nói';
    stopRecordingSession(el.p1RecordTimer);
  }

  function toggleP2Recording() {
    if (!state.speakingIsRecording) {
      el.btnP2RecordToggle.classList.add('recording');
      el.p2RecordBtnText.textContent = '⏹️ Dừng Nói Độc Thoại';
      startRecordingSession(
        el.p2TranscriptText,
        el.p2TranscriptWordCount,
        el.p2UserAudioPlayer,
        el.p2UserAudioWrap,
        el.p2RecordTimer,
        el.p2RecordTimerText
      );
    } else {
      stopP2Recording();
    }
  }

  function stopP2Recording() {
    el.btnP2RecordToggle.classList.remove('recording');
    el.p2RecordBtnText.textContent = '🎤 Bắt Đầu Nói Độc Thoại';
    stopRecordingSession(el.p2RecordTimer);
  }

  // --- PART 3: SIMULATED SPEAKING EXAM LOGIC ---

  function startSpeakingExam() {
    stopAllSpeakingAudio();

    // 1. Build test items queue
    const items = [];
    const allP1Questions = [];
    window.TOEIC_SPEAKING_DATA.part1_topics.forEach(t => {
      t.questions.forEach(q => {
        allP1Questions.push({
          type: 'p1',
          topicName: t.nameVi,
          question: q.question,
          questionVi: q.questionVi,
          prepSeconds: 30,
          speakSeconds: 45
        });
      });
    });

    const allP2Topics = window.TOEIC_SPEAKING_DATA.part2_topics.map(t => ({
      type: 'p2',
      topicName: `Đề ${t.topicNumber}: ${t.titleVi}`,
      question: t.title,
      questionVi: t.titleVi,
      cues: t.cues,
      prepSeconds: 60,
      speakSeconds: 120
    }));

    // Shuffle helper
    const shuffle = arr => arr.slice().sort(() => Math.random() - 0.5);

    if (state.speakingExamType === 'p1') {
      items.push(...shuffle(allP1Questions).slice(0, 3));
    } else if (state.speakingExamType === 'p2') {
      items.push(...shuffle(allP2Topics).slice(0, 1));
    } else {
      // Full test: 3 P1 + 1 P2
      items.push(...shuffle(allP1Questions).slice(0, 3));
      items.push(...shuffle(allP2Topics).slice(0, 1));
    }

    state.speakingExamItems = items;
    state.speakingExamItemIndex = 0;
    state.speakingExamAnswers = [];

    el.speakingExamSetup.style.display = 'none';
    el.speakingExamActive.style.display = 'flex';
    el.speakingExamResult.style.display = 'none';

    runExamStep(0);
  }

  function quitSpeakingExam() {
    stopAllSpeakingAudio();
    el.speakingExamSetup.style.display = 'flex';
    el.speakingExamActive.style.display = 'none';
    el.speakingExamResult.style.display = 'none';
  }

  function runExamStep(index) {
    if (index >= state.speakingExamItems.length) {
      showExamResults();
      return;
    }

    state.speakingExamItemIndex = index;
    const item = state.speakingExamItems[index];

    // Progress badge
    el.examStepBadge.textContent = `Câu ${index + 1} / ${state.speakingExamItems.length} (${item.type === 'p1' ? 'Phần 1: Q&A' : 'Phần 2: Mô tả'})`;

    // Display question & cues
    el.examQText.textContent = item.question;
    if (item.type === 'p2' && item.cues) {
      el.examQCues.style.display = 'grid';
      el.examQCues.innerHTML = item.cues.map((c, i) => `
        <div class="cue-card-item">
          <span class="cue-card-num">Gợi ý ${i + 1}</span>
          <span class="cue-card-en">${c.cue}</span>
        </div>
      `).join('');
    } else {
      el.examQCues.style.display = 'none';
    }

    // Step 1: Preparation Phase
    state.speakingExamPhase = 'prep';
    state.speakingExamSecondsLeft = item.prepSeconds;

    el.examPhaseBadge.className = 'exam-phase-badge prep';
    el.examPhaseBadge.textContent = '⏳ Thời gian chuẩn bị';

    el.examClockRing.className = 'exam-clock-ring';
    el.examClockNumber.textContent = state.speakingExamSecondsLeft;
    el.examClockLabel.textContent = 'giây chuẩn bị';

    el.examRecStatusText.textContent = 'Micro sẽ tự động bật khi hết thời gian chuẩn bị';
    el.examRecPulse.style.display = 'none';
    el.examTranscriptPreview.textContent = 'Đang trong thời gian chuẩn bị suy nghĩ ý tưởng...';

    el.btnSkipExamPrep.style.display = 'inline-flex';
    el.btnNextExamItem.style.display = 'none';

    playExamBeep(false);

    if (state.speakingExamInterval) clearInterval(state.speakingExamInterval);
    state.speakingExamInterval = setInterval(() => {
      state.speakingExamSecondsLeft--;
      el.examClockNumber.textContent = state.speakingExamSecondsLeft;

      if (state.speakingExamSecondsLeft <= 3 && state.speakingExamSecondsLeft > 0) {
        playExamBeep(false);
      }

      if (state.speakingExamSecondsLeft <= 0) {
        clearInterval(state.speakingExamInterval);
        state.speakingExamInterval = null;
        transitionToSpeakingPhase();
      }
    }, 1000);
  }

  function skipExamPrep() {
    if (state.speakingExamPhase === 'prep') {
      if (state.speakingExamInterval) {
        clearInterval(state.speakingExamInterval);
        state.speakingExamInterval = null;
      }
      transitionToSpeakingPhase();
    }
  }

  async function transitionToSpeakingPhase() {
    state.speakingExamPhase = 'speak';
    const item = state.speakingExamItems[state.speakingExamItemIndex];
    state.speakingExamSecondsLeft = item.speakSeconds;

    playExamBeep(true);

    el.examPhaseBadge.className = 'exam-phase-badge speak';
    el.examPhaseBadge.textContent = '🔴 Đang nói (Micro Bật)';

    el.examClockRing.className = 'exam-clock-ring speaking';
    el.examClockNumber.textContent = state.speakingExamSecondsLeft;
    el.examClockLabel.textContent = 'giây trả lời';

    el.examRecStatusText.textContent = 'Micro đang thu âm câu trả lời của bạn...';
    el.examRecPulse.style.display = 'inline-block';
    el.examTranscriptPreview.textContent = 'Bắt đầu nói ngay bây giờ...';

    el.btnSkipExamPrep.style.display = 'none';
    el.btnNextExamItem.style.display = 'inline-flex';

    // Start Recording Session for exam
    let currentExamTranscript = '';
    let currentExamAudioBlob = null;
    state.speakingAudioChunks = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      state.speakingMediaRecorder = new MediaRecorder(stream);
      state.speakingMediaRecorder.ondataavailable = e => {
        if (e.data && e.data.size > 0) state.speakingAudioChunks.push(e.data);
      };
      state.speakingMediaRecorder.onstop = () => {
        currentExamAudioBlob = new Blob(state.speakingAudioChunks, { type: 'audio/webm' });
        const blobUrl = URL.createObjectURL(currentExamAudioBlob);
        state.speakingExamAnswers.push({
          item: item,
          transcript: currentExamTranscript || '(Không nhận diện được giọng nói hoặc micro im lặng)',
          audioUrl: blobUrl
        });
        stream.getTracks().forEach(track => track.stop());
      };
      state.speakingMediaRecorder.start();
    } catch (err) {
      console.warn("Exam mic error:", err);
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      state.speakingRecognition = new SpeechRecognition();
      state.speakingRecognition.lang = 'en-US';
      state.speakingRecognition.continuous = true;
      state.speakingRecognition.interimResults = true;

      let recognized = '';
      state.speakingRecognition.onresult = (e) => {
        let interim = '';
        for (let i = e.resultIndex; i < e.results.length; ++i) {
          if (e.results[i].isFinal) recognized += e.results[i][0].transcript + ' ';
          else interim += e.results[i][0].transcript;
        }
        currentExamTranscript = (recognized + interim).trim();
        el.examTranscriptPreview.textContent = currentExamTranscript || 'Đang nghe bạn nói...';
      };
      state.speakingRecognition.start();
    }

    if (state.speakingExamInterval) clearInterval(state.speakingExamInterval);
    state.speakingExamInterval = setInterval(() => {
      state.speakingExamSecondsLeft--;
      el.examClockNumber.textContent = state.speakingExamSecondsLeft;

      if (state.speakingExamSecondsLeft <= 3 && state.speakingExamSecondsLeft > 0) {
        playExamBeep(false);
      }

      if (state.speakingExamSecondsLeft <= 0) {
        clearInterval(state.speakingExamInterval);
        state.speakingExamInterval = null;
        finishExamStep();
      }
    }, 1000);
  }

  function finishExamStep() {
    if (state.speakingExamInterval) {
      clearInterval(state.speakingExamInterval);
      state.speakingExamInterval = null;
    }

    if (state.speakingMediaRecorder && state.speakingMediaRecorder.state !== 'inactive') {
      state.speakingMediaRecorder.stop();
    }

    if (state.speakingRecognition) {
      try {
        state.speakingRecognition.stop();
      } catch (e) {}
      state.speakingRecognition = null;
    }

    // Small delay to ensure onstop finishes creating blob
    setTimeout(() => {
      runExamStep(state.speakingExamItemIndex + 1);
    }, 400);
  }

  function showExamResults() {
    stopAllSpeakingAudio();

    el.speakingExamActive.style.display = 'none';
    el.speakingExamResult.style.display = 'block';

    el.examReviewList.innerHTML = '';
    state.speakingExamAnswers.forEach((ans, idx) => {
      const itemCard = document.createElement('div');
      itemCard.className = 'exam-review-item';
      itemCard.innerHTML = `
        <div class="exam-review-q">
          <span style="color:var(--primary);">Câu ${idx + 1}:</span> ${ans.item.question}
          <div style="font-size:13px; font-weight:normal; color:var(--text-muted);">${ans.item.questionVi}</div>
        </div>
        <div class="exam-review-transcript">
          <strong>📝 Văn bản bạn đã nói:</strong> "${ans.transcript}"
        </div>
        <div>
          <strong>🎧 Nghe lại câu trả lời:</strong><br>
          <audio class="exam-review-audio" src="${ans.audioUrl}" controls></audio>
        </div>
      `;
      el.examReviewList.appendChild(itemCard);
    });
  }


    // Start app on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', init);

})();
