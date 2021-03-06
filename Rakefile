task :default => :build

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
    post.puts "- linux"
    post.puts "- fedora"
    post.puts "---"
    post.puts "{{ page.title }}"
    post.puts "================"
  end
  system("/usr/bin/vim #{filename}")
end
task :new_post => :post

desc 'Prepare images directory'
task :img do
  latest_file = Dir.open("_posts") {|d| 
    d.max_by {|f| 
      if f =~ /^\..*/
        Time.at(0)
      else
        File.mtime(File.join("_posts", f))
      end
    }
  }
  newdir = "assets/img/posts/" + latest_file.to_s.gsub(/\.\w+$/, '')
  FileUtils.mkdir_p newdir
  puts newdir
end

desc 'Clean up generated site'
task :clean do
  cleanup
end

desc 'Build site with Jekyll'
task :build do
  jekyll('build')
end

desc 'Start server with --auto'
task :server => :clean do
  jekyll('server --watch')
end

desc 'Build and deploy'
task :deploy => :build do
  sh 'rsync -rtzh --progress --delete _site/ username@servername:/var/www/websitename/'
end

desc 'Check links for site already running on localhost:4000'
task :check_links do
  begin
    require 'anemone'
    root = 'http://localhost:4000/'
    Anemone.crawl(root, :discard_page_bodies => true) do |anemone|
      anemone.after_crawl do |pagestore|
        broken_links = Hash.new { |h, k| h[k] = [] }
        pagestore.each_value do |page|
          if page.code != 200
            referrers = pagestore.pages_linking_to(page.url)
            referrers.each do |referrer|
              broken_links[referrer] << page
            end
          end
        end
        broken_links.each do |referrer, pages|
          puts "#{referrer.url} contains the following broken links:"
          pages.each do |page|
            puts "  HTTP #{page.code} #{page.url}"
          end
        end
      end
    end

  rescue LoadError
    abort 'Install anemone gem: gem install anemone'
  end
end

def cleanup
  sh 'rm -rf _site'
end

def jekyll(opts = '')
  sh 'jekyll ' + opts
end
