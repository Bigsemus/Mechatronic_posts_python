from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data - Replace this with a proper data storage solution
articles_data = [
    {'id': 1, 'title': 'Sample Article 1', 'content': 'This is a sample article content.'},
    {'id': 2, 'title': 'Sample Article 2', 'content': 'This is another sample article content.'},
]

@app.route('/')
def index():
    return render_template('index.html', articles=articles_data)

@app.route('/article/<int:article_id>')
def article(article_id):
    article = next((a for a in articles_data if a['id'] == article_id), None)
    if article:
        return render_template('article.html', article=article)
    else:
        return "Article not found", 404

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_content = request.form.get('content')

        # Generate a unique ID for the new article
        new_article_id = len(articles_data) + 1

        # Create a new article and add it to the data
        new_article = {'id': new_article_id, 'title': new_title, 'content': new_content}
        articles_data.append(new_article)

        # Redirect to the newly created article
        return redirect(url_for('article', article_id=new_article_id))

    return render_template('create_post.html')

@app.route('/edit_post/<int:article_id>', methods=['GET', 'POST'])
def edit_post(article_id):
    article = next((a for a in articles_data if a['id'] == article_id), None)
    if not article:
        return "Article not found", 404

    if request.method == 'POST':
        article['title'] = request.form.get('title')
        article['content'] = request.form.get('content')

        return redirect(url_for('article', article_id=article_id))

    return render_template('edit_post.html', article=article)

@app.route('/delete_post/<int:article_id>', methods=['GET', 'POST', 'DELETE'])
def delete_post(article_id):
    global articles_data

    if request.method == 'GET':
        # Display confirmation page
        article = next((a for a in articles_data if a['id'] == article_id), None)
        if article:
            return render_template('delete_post.html', article=article)
        else:
            return "Article not found", 404

    elif request.method == 'POST':
        # Perform deletion
        articles_data = [a for a in articles_data if a['id'] != article_id]
        return redirect(url_for('index'))

    elif request.method == 'DELETE':
        # Perform deletion for the fetch API
        articles_data = [a for a in articles_data if a['id'] != article_id]
        return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
