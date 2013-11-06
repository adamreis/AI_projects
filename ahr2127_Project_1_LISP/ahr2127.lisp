
(defun match (p d)
	(rpm p d '())
)

(defun rpm (p d a)
	(cond
		((or (and (null p) (null d)) (equal p '(*))) ;we've exhausted both successfully or p is (*)
			(cond (a a) (t t)) ;return either association list or T
		)

		((or (null p) (null d)) ;if we've only exhausted one, return nil
			nil
		)

		((equal (car p) '?) ;lone question mark
			(rpm (cdr p) (cdr d) a)
		)

		((is-not (first p)) ;exlamation mark 
			(let ((v (var-binding (first p))))
				(cond
					;make sure the bound variable is not the one you're testing against
					((equal (car d) (car (cdr (assoc v a))))
						nil
					)
					(t (rpm (cdr p) (cdr d) a))
				)
			)
		)

		((is-less (first p)) ;less than
			(let ((v (var-binding (first p))))
				(cond
					((or (not (numberp (car (cdr (assoc v a))))) (>= (car d) (car (cdr (assoc v a)))) )
						nil
					)
					(t (rpm (cdr p) (cdr d) a))
				)
			)
		)

		((is-greater (first p)) ;greater than
			(let ((v (var-binding (first p))))
				(cond
					((or (not (numberp (car (cdr (assoc v a))))) (<= (car d) (car (cdr (assoc v a)))) )
						nil
					)
					(t (rpm (cdr p) (cdr d) a))
				)
			)
		)

		((is-ampersand (first p)) ;ampersand
			(let ((equation (cdr (first p))) (valid t))
				;loop for every argument in the & list, running rpm just on that
				;element and the first element of d to see if they match
				(loop for x in equation do 
					(setq valid (and valid (rpm (cons x '()) (cons (first d) '()) a)))
				)
				(cond
					(valid
						(rpm (cdr p) (cdr d) a)
					)
					(t nil)
				)
			)
		)

		((is-vbl (first p)) ;we've encountered a pattern variable:
			(cond
				((assoc (first p) a) ;its a bound variable:
					(cond
						;if its bound value is equal to the 
						;first data element, we return the 
						;real pattern match of the rest of the 
						;pattern with the rest of the data 
						((eql (car d) (car (cdr (assoc (first p) a))))
							(rpm (rest p)(rest d) a))
						(t 
							nil
						)
					)
				)
				;if its unbound, we bind it on the 
				;association list and similarly call 
				;rpm recursively.
				((eql (car d) nil)
					a
				) 
				(t (rpm (rest p)(rest d) (cons (list (first p) (first d)) a))) 
			)
		)
		((eq '* (first p)) 
			;Kleene Star matches 0 or more elements, so... 
			(let((zero (rpm (rest p) d a)) (one (rpm p (rest d) a))) ;check for 0 and 1 separately
				(cond
					((and (not zero) (not one)) ;if both are nil, return nil
						nil
					)
					((not zero) ;if one is nil, return the other
						one
					)
					((not one)
						zero
					)
					(t ;if neither is nill, add both (as their own lists) to the big list
						(append (cons zero '()) (cons one '()))
					)
				)
			)
		)
		(t ;otherwise, do a normal comparison between elements to see if they're the same
			(let ((pp (car p)) (dd (car d))) 
				(cond 
					((and (listp pp) (listp dd)) 
						(and (rpm pp dd a) (rpm (cdr p) (cdr d) a))
					) 
					(t 
						(and (eq pp dd) (rpm (cdr p) (cdr d) a))
					)
				)
			)
		)
	)
)

(defun is-vbl (v)
	"does it start with ?"
  (and (symbolp v) (equal (elt (symbol-name v) 0) #\?))
)

(defun is-not (v)
	"does it start with !"
	(and (symbolp v) (equal (elt (symbol-name v) 0) #\!))
)

(defun is-less (v)
	"does it start with <"
	(and (symbolp v) (equal (elt (symbol-name v) 0) #\<))
)

(defun is-greater (v)
	"does it start with >"
	(and (symbolp v) (equal (elt (symbol-name v) 0) #\>))
)

(defun var-binding (v)
	"return variable bound to b"
	(intern (concatenate 'string "?" (subseq (symbol-name v) 1)))
)

(defun is-ampersand (v)
	"is it &"
	(and (listp v) (equal (car v) '&))
)
