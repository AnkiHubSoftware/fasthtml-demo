from fasthtml.common import *
from monsterui.all import *
import yaml
from pathlib import Path

app, rt = fast_app(hdrs=Theme.blue.headers())

bookmarked_posts = []

def get_meta(post_path):
    "Extract metadata from a blog post markdown file."
    with open(post_path, 'r') as f: content = f.read()
    content = content.split('---')[1]
    return yaml.safe_load(content)

def get_post_content(post_path):
    "Extract both metadata and content from a blog post markdown file."
    with open(post_path, 'r') as f: content = f.read()
    parts = content.split('---')
    metadata = yaml.safe_load(parts[1])
    content = parts[2] if len(parts) > 2 else ""
    return metadata, content

def get_posts():
    return [Path(p) for p in Path('posts').glob('*.md')]

def BlogCard(post_path):
    metadata, content = get_post_content(post_path)
    
    tags = [Span(tag, cls="px-2 py-1 mr-1 text-xs rounded bg-blue-100 text-blue-800") for tag in metadata.get('tags', [])]
    
    # Truncate content to create a preview (first 150 characters)
    preview_content = content.strip()[:150] + "..." if len(content.strip()) > 150 else content.strip()
    
    # Check if this post is bookmarked
    is_bookmarked = post_path.stem in bookmarked_posts
    bookmark_icon = "star-fill" if is_bookmarked else "star"
    icon_color = "text-green-500" if is_bookmarked else "text-gray-400"
    bookmark_id = f"bookmark-{post_path.stem}"
    
    return Card(
        # Image header if available
        Img(src=metadata.get('image'), alt=metadata.get('title'), cls="w-full h-48 object-cover") if 'image' in metadata else None,
        
        # Card content
        Div(
            DivFullySpaced(
                Span(metadata.get('category', ''), cls="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800"),
                Button(
                    UkIcon(bookmark_icon, height=20, cls=icon_color),
                    hx_post=toggle_bookmark.to(slug=post_path.stem),
                    hx_swap="outerHTML",
                    id=bookmark_id,
                    cls=ButtonT.ghost
                )
            ),
            H3(metadata.get('title', ''), cls="mt-2 mb-1"),
            
            P(
                f"By {metadata.get('author', '')} on {metadata.get('date', '')}", 
                cls=TextPresets.muted_sm
            ),
            P(metadata.get('description', preview_content), cls="my-3"),
            
            Div(*tags, cls="mt-2"),
            
            cls="p-4"
        ),
        
        # Card footer with read more link - using query parameter instead of path parameter
        footer=A(
            "Read More →", 
            href=f"/post?slug={post_path.stem}",
            cls=f"{AT.text} {TextT.right} block"
        ),
        
        cls=CardT.hover
    )

@rt
def index():
    return Titled(
        "My Blog",
        DivFullySpaced(
            H2("Latest Posts"),
            A("View Bookmarked", href="/bookmarked", cls=AT.primary)
        ),
        Div(*[BlogCard(p) for p in get_posts()])
    )

@rt
def post(slug: str):
    """Render a single blog post by its slug (filename without extension)"""
    # Find the post file that matches the slug
    post_path = Path(f'posts/{slug}.md')
    print(post_path)
    # Get post metadata and content
    metadata, content = get_post_content(post_path)
    return Container(render_md(content))

@rt
def toggle_bookmark(slug: str):
    """Toggle bookmark status for a post"""
    if slug in bookmarked_posts:
        bookmarked_posts.remove(slug)
        bookmark_icon = "star"
        icon_color = "text-gray-400"
    else:
        bookmarked_posts.append(slug)
        bookmark_icon = "star"
        icon_color = "text-green-500"
    
    bookmark_id = f"bookmark-{slug}"
    
    return Button(
        UkIcon(bookmark_icon, height=20, cls=icon_color),
        hx_post=toggle_bookmark.to(slug=slug),
        hx_swap="outerHTML",
        id=bookmark_id,
        cls=ButtonT.ghost
    )

@rt
def bookmarked():
    """Show only bookmarked posts"""
    # Filter posts to only show bookmarked ones
    bookmarked_post_paths = [p for p in get_posts() if p.stem in bookmarked_posts]
    
    return Titled(
        "Bookmarked Posts",
        DivFullySpaced(
            H2("Your Bookmarked Posts"),
            A("View All Posts", href="/", cls=AT.primary)
        ),
        Div(
            P("You haven't bookmarked any posts yet.", cls=TextPresets.muted_lg) if not bookmarked_post_paths 
            else Div(*[BlogCard(p) for p in bookmarked_post_paths])
        ),
        A("View All Posts", href="/", cls=f"{AT.primary} mt-4 inline-block")
    )

serve()