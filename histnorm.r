' @noRd
#' @exportMethod hist.norm
#' @export
hist.norm <- function(x,
                         breaks = "Sturges",
                         freq = NULL,
                         include.lowest = TRUE,
                         normalcurve = TRUE,
                         right = TRUE,
                         density = NULL,
                         angle = 45,
                         col = NULL,
                         border = NULL,
                         main = paste("Histogram of", xname),
                         ylim = NULL,
                         xlab = xname,
                         ylab = NULL,
                         axes = TRUE,
                         plot = TRUE,
                         labels = FALSE,
                         warn.unused = TRUE,
                         ...)  {

  # https://stackoverflow.com/a/20078645/4575331
  xname <- paste(deparse(substitute(x), 500), collapse = "\n")

  suppressWarnings(
    h <- graphics::hist.default(
      x = x,
      breaks = breaks,
      freq = freq,
      include.lowest = include.lowest,
      right = right,
      density = density,
      angle = angle,
      col = col,
      border = border,
      main = main,
      ylim = ylim,
      xlab = xlab,
      ylab = ylab,
      axes = axes,
      plot = plot,
      labels = labels,
      warn.unused = warn.unused,
      ...
    )
  )

  if (normalcurve == TRUE & plot == TRUE) {
    x <- x[!is.na(x)]
    xfit <- seq(min(x), max(x), length = 40)
    yfit <- dnorm(xfit, mean = mean(x), sd = sd(x))
    if (isTRUE(freq) | (is.null(freq) & is.null(density))) {
      yfit <- yfit * diff(h$mids[1:2]) * length(x)
    }
    lines(xfit, yfit, col = "black", lwd = 2)
  }

  if (plot == TRUE) {
    invisible(h)
  } else {
    h
  }
}
