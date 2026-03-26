from sqlalchemy import inspect, text


COLUMN_DEFINITIONS = {
    "hero_banners": {
        "media_type": "VARCHAR(20)",
        "video_url": "VARCHAR(500)",
        "title_font_size": "INTEGER",
        "subtitle_font_size": "INTEGER",
        "description_font_size": "INTEGER",
        "text_position": "VARCHAR(40)",
    },
    "site_sections": {
        "parent_id": "INTEGER",
        "node_type": "VARCHAR(20)",
        "content_source": "VARCHAR(20)",
        "summary": "VARCHAR(500)",
        "group_key": "VARCHAR(80)",
        "media_type": "VARCHAR(20)",
        "video_url": "VARCHAR(500)",
        "pinned_at": "DATETIME",
    },
    "products": {
        "media_type": "VARCHAR(20)",
        "video_url": "VARCHAR(500)",
        "pinned_at": "DATETIME",
    },
    "news_articles": {
        "media_type": "VARCHAR(20)",
        "video_url": "VARCHAR(500)",
        "pinned_at": "DATETIME",
    },
}


def relax_legacy_constraints(connection) -> None:
    dialect = connection.dialect.name
    if dialect == "mysql":
        connection.execute(text("ALTER TABLE hero_banners MODIFY COLUMN image_url VARCHAR(500) NULL"))
    elif dialect == "postgresql":
        connection.execute(text("ALTER TABLE hero_banners ALTER COLUMN image_url DROP NOT NULL"))


def ensure_legacy_columns(engine) -> None:
    """Add new columns and backfill defaults for legacy deployments without migrations."""
    inspector = inspect(engine)
    with engine.begin() as connection:
        for table_name, columns in COLUMN_DEFINITIONS.items():
            existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, column_type in columns.items():
                if column_name in existing_columns:
                    continue
                connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))

        relax_legacy_constraints(connection)

        connection.execute(
            text(
                """
                UPDATE hero_banners
                SET
                    media_type = COALESCE(media_type, 'image'),
                    title_font_size = COALESCE(title_font_size, 72),
                    subtitle_font_size = COALESCE(subtitle_font_size, 13),
                    description_font_size = COALESCE(description_font_size, 17),
                    text_position = COALESCE(text_position, 'left-center')
                """
            )
        )
        connection.execute(
            text(
                """
                UPDATE site_sections
                SET
                    parent_id = parent_id,
                    node_type = COALESCE(node_type, 'content'),
                    content_source = COALESCE(content_source, 'section'),
                    summary = COALESCE(summary, body),
                    group_key = CASE
                        WHEN group_key IS NOT NULL AND group_key != '' THEN group_key
                        WHEN `key` IN ('core_selling', 'brand_story', 'revitalization', 'product_intro', 'news_intro') THEN `key`
                        ELSE group_key
                    END,
                    media_type = COALESCE(media_type, 'image'),
                    sort_order = CASE
                        WHEN COALESCE(node_type, 'content') = 'content' AND COALESCE(sort_order, 0) <= 0 AND pinned_at IS NULL THEN 1
                        ELSE COALESCE(sort_order, 0)
                    END,
                    pinned_at = CASE
                        WHEN COALESCE(node_type, 'content') = 'content' AND COALESCE(sort_order, 0) <= 0 AND pinned_at IS NULL THEN NULL
                        ELSE pinned_at
                    END
                """
            )
        )
        connection.execute(
            text(
                """
                UPDATE products
                SET
                    media_type = COALESCE(media_type, 'image'),
                    sort_order = CASE
                        WHEN COALESCE(sort_order, 0) <= 0 AND pinned_at IS NULL THEN 1
                        ELSE COALESCE(sort_order, 0)
                    END,
                    pinned_at = CASE
                        WHEN COALESCE(sort_order, 0) <= 0 AND pinned_at IS NULL THEN NULL
                        ELSE pinned_at
                    END
                """
            )
        )
        connection.execute(
            text(
                """
                UPDATE news_articles
                SET
                    media_type = COALESCE(media_type, 'image'),
                    sort_order = CASE
                        WHEN COALESCE(sort_order, 0) <= 0 AND pinned_at IS NULL THEN 1
                        ELSE COALESCE(sort_order, 0)
                    END,
                    pinned_at = CASE
                        WHEN COALESCE(sort_order, 0) <= 0 AND pinned_at IS NULL THEN NULL
                        ELSE pinned_at
                    END
                """
            )
        )
