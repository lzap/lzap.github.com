---
type: "post"
aliases:
- /2012/07/migrated-to-github.html
date: "2012-07-24T00:00:00Z"
tags:
- blog
title: Blog migrated to github.com
---

You maybe noticed some articles in your RSS reader are doubled and I apologize
for that. I have successfully migrated to the new blog hosting and engine and
switched the FeedBurner RSS source.

My blog is now just a bunch of static pages server by github.com pages and you
may noticed is is quite fast. I use
[Jekyll](https://github.com/mojombo/jekyll/) for generating of the content. I
was playing around with various addons and forks, but then I went for this
plain approach together with [Twitter
Bootstrap](https://github.com/mojombo/jekyll/) template.

Before I started with migration, I wanted to be absolutely sure links will not
change. I found nice script for migration of a Blogger XML export to Jekyll
compatible files, so I have improved it a bit to store filenames in the format
compatible with Blogger links. It's called
[blogger2jekyll.rb](https://gist.github.com/3172705).

Actual migration was as easy as running

    ruby blogger2jekyll.rb export-file.xml

For those who would like to use my script, please note I have commented out
section for Blogger-based comments since I don't use it. And make sure you set
permalink configuration variable to

{{< highlight yaml >}}
title : Lukas Zapletal
tagline: linux - life - live!
permalink: /:categories/:year/:month/:title.html
{{< / highlight >}}

Creating layout and templates was piece of cake since I did not use any
dynamic features of Blogger and my comments were already using Disqus. Few
pages were also just copy and paste. The last thing was to change DNS and RSS.
I also slightly modified a rake task for creating new posts:

{{< highlight ruby >}}
desc "Begin a new post"
task :post do
  title = ENV["title"] || "new-post"
  slug = title.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
  begin
    date = (ENV['date'] ? Time.parse(ENV['date']) : Time.now).strftime('%Y-%m-%d')
  rescue Exception => e
    abort("Error - date format must be YYYY-MM-DD, please check you typed it correctly!")
  end
  filename = File.join('_posts', "#{date}-#{slug}.mkd")
  if File.exist?(filename)
    abort("rake aborted filename already exists!")
  end
  
  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: post"
    post.puts "title: \"#{title.gsub(/-/,' ')}\""
    post.puts "date: #{date}"
    post.puts "tags:"
    post.puts "---"
    post.puts "{ { page.title } }" # remove spaces between { and }
    post.puts "================"
  end
  system("/usr/bin/gvim #{filename}")
end
{{< / highlight >}}

I highly recommend github.com pages. If you are a geek, if you like git, then
there is nothing better for simple static pages or even blogs. I hope you will
like it.
