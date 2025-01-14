import heapq

class PopularBook:

    @staticmethod
    def add_book_to_queue(queue, book ,requests):
        heapq.heappush(queue, (-requests, book))
        heapq.heapify(queue)

    @staticmethod
    def peek_most_popular(queue,i):
        if not queue:
            return None
        return queue[i]

    @staticmethod
    def get_most_popular(queue):
        popular_list=[]
        n=10
        if not queue:
            return None
        for i in range(n):
            book=queue.peek_most_popular(i)
            popular_list.append(book)
        return popular_list

    @staticmethod
    def update_book_popularity(queue, book ,requests):
        book_found = False
        for i in range(len(queue)):
            title = queue[i]
            if title == book.title:
                queue[i] = (book, -requests)
                book_found = True
                break
        if not book_found:
            print(f"Book '{book.title}' not found!")
            return
        heapq.heapify(queue)