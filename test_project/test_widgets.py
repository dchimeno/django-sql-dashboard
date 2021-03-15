def test_big_number_widget(admin_client, dashboard_db):
    response = admin_client.post(
        "/dashboard/",
        {"sql": "select 'Big' as label, 10801 * 5 as big_number"},
        follow=True,
    )
    html = response.content.decode("utf-8")
    assert "<p>Big</p>\n  <h1>54005</h1>" in html


def test_markdown_widget(admin_client, dashboard_db):
    response = admin_client.post(
        "/dashboard/",
        {"sql": "select '# Foo\n\n## Bar [link](/)' as markdown"},
        follow=True,
    )
    html = response.content.decode("utf-8")
    assert '<h1>Foo</h1>\n<h2>Bar <a href="/" rel="nofollow">link</a></h2>' in html


def test_html_widget(admin_client, dashboard_db):
    response = admin_client.post(
        "/dashboard/",
        {
            "sql": "select '<h1>Hi</h1><script>alert(\"evil\")</script><p>There</p>' as markdown"
        },
        follow=True,
    )
    html = response.content.decode("utf-8")
    assert (
        "<h1>Hi</h1>\n" '&lt;script&gt;alert("evil")&lt;/script&gt;\n' "<p>There</p>"
    ) in html


def test_bar_chart_widget(admin_client, dashboard_db):
    sql = """
    SELECT * FROM (
        VALUES (1, 'one'), (2, 'two'), (3, 'three')
    ) AS t (bar_quantity, bar_label);
    """
    response = admin_client.post(
        "/dashboard/",
        {"sql": sql},
        follow=True,
    )
    html = response.content.decode("utf-8")
    assert (
        '<script id="vis-data-0" type="application/json">'
        '[{"bar_quantity": 1, "bar_label": "one"}, '
        '{"bar_quantity": 2, "bar_label": "two"}, '
        '{"bar_quantity": 3, "bar_label": "three"}]</script>'
    ) in html
    assert '$schema: "https://vega.github.io/schema/vega-lite/v5.json"' in html
