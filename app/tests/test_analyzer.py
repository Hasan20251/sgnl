import pytest
from app.services.analyzer import HeuristicAnalyzer


class TestHeuristicAnalyzer:
    """Test HeuristicAnalyzer class methods."""

    def test_init(self):
        """Test analyzer initialization and regex compilation."""
        analyzer = HeuristicAnalyzer()
        assert analyzer.affiliate_regex is not None
        assert analyzer.hype_regex is not None

        # Test regex patterns
        assert analyzer.affiliate_regex.search("amzn.to/link")
        assert analyzer.hype_regex.search("shocking news")

    def test_calculate_structure_score_valid_html(self, sample_html):
        """Test structure score calculation with valid HTML."""
        analyzer = HeuristicAnalyzer()
        result = analyzer.calculate_structure_score(sample_html, "machine learning")

        assert isinstance(result, dict)
        assert "score" in result
        assert "reason" in result
        assert "adjustments" in result
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100

    def test_calculate_structure_score_empty_html(self):
        """Test structure score calculation with empty HTML."""
        analyzer = HeuristicAnalyzer()
        result = analyzer.calculate_structure_score("", "test")

        assert result["score"] == 0
        assert "Empty or too short content" in result["reason"]

    def test_calculate_structure_score_short_html(self):
        """Test structure score calculation with short HTML."""
        short_html = "<html><body>Short</body></html>"
        analyzer = HeuristicAnalyzer()
        result = analyzer.calculate_structure_score(short_html, "test")

        assert result["score"] == 0
        assert "Empty or too short content" in result["reason"]

    def test_calculate_structure_score_parse_error(self):
        """Test structure score calculation with malformed HTML."""
        malformed_html = "<html><unclosed><tags>content"
        analyzer = HeuristicAnalyzer()
        result = analyzer.calculate_structure_score(malformed_html, "test")

        assert result["score"] == 30
        assert "Failed to parse HTML" in result["reason"]

    def test_analyze_code_density_with_code(self, sample_html):
        """Test code density analysis with HTML containing code."""
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._analyze_code_density(analyzer, "machine learning code")

        assert score > 0
        assert "code" in reason.lower()

    def test_analyze_code_density_no_code(self):
        """Test code density analysis with HTML containing no code."""
        html_no_code = "<html><body><p>This is just plain text content.</p></body></html>"
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._analyze_code_density(analyzer, "plain text")

        assert score == 0
        assert reason == ""

    def test_analyze_data_density_with_tables(self, sample_html):
        """Test data density analysis with HTML containing tables."""
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._analyze_data_density(analyzer)

        assert score > 0
        assert "table" in reason.lower()

    def test_analyze_data_density_no_tables(self):
        """Test data density analysis with HTML containing no tables."""
        html_no_tables = "<html><body><p>No tables here.</p></body></html>"
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._analyze_data_density(analyzer)

        assert score == 0
        assert reason == ""

    def test_detect_slop_high_ratio(self):
        """Test slop detection with high HTML-to-text ratio."""
        # Create HTML with lots of markup and little text
        bloated_html = "<div><span><em><strong><a href='#'>click</a></strong></em></span></div>" * 50
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._detect_slop(bloated_html, analyzer)

        assert score < 0
        assert "bloated" in reason.lower() or "ratio" in reason.lower()

    def test_detect_slop_clean_content(self):
        """Test slop detection with clean, text-focused content."""
        clean_html = "<html><body><p>This is clean text content with minimal markup.</p></body></html>"
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._detect_slop(clean_html, analyzer)

        assert score >= 0

    def test_detect_slop_no_text(self):
        """Test slop detection with HTML containing no readable text."""
        no_text_html = "<html><body><img src='test.jpg'><script>alert('test');</script></body></html>"
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._detect_slop(no_text_html, analyzer)

        assert score < 0
        assert "readable text" in reason.lower()

    def test_detect_affiliates_with_affiliate_links(self):
        """Test affiliate detection with affiliate links."""
        html_with_affiliates = """
        <html><body>
        <a href="amzn.to/test">Buy now</a>
        <a href="shareasale.com/aff">Affiliate link</a>
        <a href="example.com/normal">Normal link</a>
        </body></html>
        """
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._detect_affiliates(analyzer)

        assert score < 0
        assert "affiliate" in reason.lower()

    def test_detect_affiliates_no_affiliate_links(self, sample_html):
        """Test affiliate detection with no affiliate links."""
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._detect_affiliates(analyzer)

        assert score == 0
        assert reason == ""

    def test_detect_hype_with_hype_title(self):
        """Test hype detection with clickbait title."""
        html_hype = "<html><head><title>You won't believe this shocking secret!</title></head><body></body></html>"
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._detect_hype(analyzer)

        assert score < 0
        assert "clickbait" in reason.lower() or "hype" in reason.lower()

    def test_detect_hype_with_hype_h1(self):
        """Test hype detection with clickbait H1."""
        html_hype = "<html><body><h1>Mind-blowing revolutionary breakthrough!</h1></body></html>"
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._detect_hype(analyzer)

        assert score < 0
        assert "headline" in reason.lower() or "hype" in reason.lower()

    def test_detect_hype_no_hype(self, sample_html):
        """Test hype detection with normal title."""
        analyzer = HeuristicAnalyzer()
        score, reason = analyzer._detect_hype(analyzer)

        assert score == 0
        assert reason == ""

    def test_calculate_structure_score_adjustments(self, sample_html):
        """Test that adjustments are properly tracked."""
        analyzer = HeuristicAnalyzer()
        result = analyzer.calculate_structure_score(sample_html, "machine learning")

        assert "adjustments" in result
        assert isinstance(result["adjustments"], list)

        # Each adjustment should be a tuple of (score_change, reason)
        for adjustment in result["adjustments"]:
            assert isinstance(adjustment, tuple)
            assert len(adjustment) == 2
            assert isinstance(adjustment[0], int)
            assert isinstance(adjustment[1], str)</content>
<parameter name="filePath">app/tests/test_analyzer.py