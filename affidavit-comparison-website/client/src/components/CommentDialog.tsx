import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { MessageSquare, Trash2, Send } from "lucide-react";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";

interface CommentDialogProps {
  sectionNumber: string;
  paragraphNumber: string;
  paragraphType: "AD" | "JR" | "DR";
}

export function CommentDialog({ sectionNumber, paragraphNumber, paragraphType }: CommentDialogProps) {
  const [open, setOpen] = useState(false);
  const [newComment, setNewComment] = useState("");
  const [author, setAuthor] = useState("");

  const utils = trpc.useUtils();
  
  // Fetch comments for this paragraph
  const { data: comments = [], isLoading } = trpc.comments.getAll.useQuery(
    { sectionNumber, paragraphNumber, paragraphType },
    { enabled: open }
  );

  // Add comment mutation
  const addCommentMutation = trpc.comments.add.useMutation({
    onSuccess: () => {
      toast.success("Comment added successfully");
      setNewComment("");
      utils.comments.getAll.invalidate();
    },
    onError: (error) => {
      toast.error(`Failed to add comment: ${error.message}`);
    },
  });

  // Delete comment mutation
  const deleteCommentMutation = trpc.comments.delete.useMutation({
    onSuccess: () => {
      toast.success("Comment deleted successfully");
      utils.comments.getAll.invalidate();
    },
    onError: (error) => {
      toast.error(`Failed to delete comment: ${error.message}`);
    },
  });

  const handleAddComment = () => {
    if (!newComment.trim()) {
      toast.error("Comment cannot be empty");
      return;
    }

    addCommentMutation.mutate({
      sectionNumber,
      paragraphNumber,
      paragraphType,
      content: newComment,
      author: author.trim() || undefined,
    });
  };

  const handleDeleteComment = (id: number) => {
    if (confirm("Are you sure you want to delete this comment?")) {
      deleteCommentMutation.mutate({ id });
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <MessageSquare className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle>
            Comments for {paragraphType} {paragraphNumber}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {/* Existing Comments */}
          <div>
            <h4 className="text-sm font-semibold mb-2">
              {comments.length} {comments.length === 1 ? "Comment" : "Comments"}
            </h4>
            <ScrollArea className="h-64 border rounded-md p-4">
              {isLoading ? (
                <div className="text-center text-sm text-muted-foreground">Loading comments...</div>
              ) : comments.length === 0 ? (
                <div className="text-center text-sm text-muted-foreground">
                  No comments yet. Be the first to add one!
                </div>
              ) : (
                <div className="space-y-4">
                  {comments.map((comment) => (
                    <div key={comment.id} className="border-b pb-3 last:border-0">
                      <div className="flex items-start justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-medium">{comment.author}</span>
                          <span className="text-xs text-muted-foreground">
                            {new Date(comment.createdAt).toLocaleString()}
                          </span>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6"
                          onClick={() => handleDeleteComment(comment.id)}
                        >
                          <Trash2 className="h-3 w-3 text-destructive" />
                        </Button>
                      </div>
                      <p className="text-sm whitespace-pre-wrap">{comment.content}</p>
                    </div>
                  ))}
                </div>
              )}
            </ScrollArea>
          </div>

          {/* Add New Comment */}
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">Add a Comment</h4>
            <Input
              placeholder="Your name (optional)"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              className="mb-2"
            />
            <Textarea
              placeholder="Write your comment or annotation..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              rows={4}
            />
            <div className="flex justify-end">
              <Button
                onClick={handleAddComment}
                disabled={addCommentMutation.isPending || !newComment.trim()}
              >
                <Send className="w-4 h-4 mr-2" />
                {addCommentMutation.isPending ? "Adding..." : "Add Comment"}
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
